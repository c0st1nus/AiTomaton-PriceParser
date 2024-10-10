import pymysql
import argparse

def add_columns_to_tables(columns):
    conn = pymysql.connect(host='145.249.249.29', user='remoteuser', password='new_strong_password', database='parser')
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    exception = ["average_prices"]

    for table in tables:
        table_name = table[0]
        if table_name in exception:
            continue
        cursor.execute(f"DESCRIBE {table_name}")
        existing_columns = cursor.fetchall()
        existing_column_names = [column[0] for column in existing_columns]
        for column_name, column_type in columns.items():
            if column_name not in existing_column_names:
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")

    conn.commit()
    conn.close()

def remove_columns_from_tables(columns):
    conn = pymysql.connect(host='145.249.249.29', user='remoteuser', password='new_strong_password', database='parser')
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    exception = ["average_prices"]

    for table in tables:
        table_name = table[0]
        if table_name in exception:
            continue
        cursor.execute(f"DESCRIBE {table_name}")
        existing_columns = cursor.fetchall()
        existing_column_names = [column[0] for column in existing_columns]
        for column_name in columns:
            if column_name in existing_column_names:
                cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Example usage: python new_lines.py add -c MMLU:VARCHAR(255) LLMArena:VARCHAR(255)
    parser = argparse.ArgumentParser(description="Add or remove columns from MySQL tables.")
    parser.add_argument("-c", required=True, nargs='+', help="List of columns to add or remove in the format 'column_name:column_type'")
    parser.add_argument("action", choices=["add", "rm"], help="Action to perform: 'add' to add columns, 'rm' to remove columns")

    args = parser.parse_args()

    columns = {}
    for column in args.c:
        if ':' not in column:
            name = column
            type_ = 'VARCHAR(255)'
        else:
            name, type_ = column.split(':', 1)
        columns[name] = type_

    if args.action == "add":
        add_columns_to_tables(columns)
    elif args.action == "rm":
        remove_columns_from_tables(columns)