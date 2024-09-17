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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add columns to MySQL tables.")
    parser.add_argument("--c", required=True, nargs='+', help="List of columns to add in the format 'column_name:column_type'")

    args = parser.parse_args()

    columns = {}
    for column in args.c:
        if ':' not in column:
            name = column
            type_ = 'VARCHAR(255)'
        else:
            name, type_ = column.split(':', 1)
        columns[name] = type_

    add_columns_to_tables(columns)