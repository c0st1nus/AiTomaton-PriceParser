import pymysql
import openpyxl
import concurrent.futures
import argparse
from io import BytesIO

def generate_table(date):
    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'database': 'parser'
    }

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()
    conn.close()

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Selected Rows"

    columns_to_check = [
        'openrouter', 'groq', 'mistral', 'cohere', 'openAI', 
        'anthropic', 'google', 'microsoft', 'deepseek', 'cloudflare', 'novita', 
        'fireworks', 'replicate', 'MMLU', 'LLMArena', 
    ]

    sheet.append(["Table Name", "date"] + columns_to_check)

    def process_table(table_name):
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} WHERE date >= '{date}'")
        rows = cursor.fetchall()
        for row in rows:
            row_data = [table_name] + list(row)
            sheet.append(row_data)
        cursor.close()
        conn.close()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_table, table[0]): table[0] for table in tables}
        for future in concurrent.futures.as_completed(futures):
            future.result()

    # Сохранение таблицы в объект BytesIO
    output = BytesIO()
    workbook.save(output)
    output.seek(0)
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some tables.')
    parser.add_argument('-d', '--date', type=str, required=True, help='Дата в формате "YYYY-MM-DD HH:MM:SS"')
    args = parser.parse_args()

    workbook = generate_table(args.date)
    with open("selected_rows.xlsx", "wb") as f:
        f.write(workbook.getvalue())