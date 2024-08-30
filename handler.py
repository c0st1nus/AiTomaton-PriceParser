import json
import re
import pymysql
from datetime import datetime

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='parser',
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)

def get_mysql_type(value):
    if isinstance(value, int):
        return 'INT'
    elif isinstance(value, float):
        return 'FLOAT'
    elif isinstance(value, bool):
        return 'BOOLEAN'
    else:
        return 'VARCHAR(255)'

def clean_column_name(name):
    name = re.sub(r'[^0-9a-zA-Z_]', '_', name)
    if name[0].isdigit():
        name = 'col_' + name
    return name

def create_data_queries(data, average_prices):
    queries = []
    for key, value in data.items():
        query = f"INSERT INTO {clean_column_name(key)} (date, "
        for operator in value.keys():
            query += f"{clean_column_name(operator)}, "
        query = query.rstrip(", ")
        query += ") VALUES (NOW(), "
        for operator, value2 in value.items():
            query += f"'{value2['input_price']}/{value2['output_price']}', "
        query = query.rstrip(", ")
        query += ")"
        queries.append(query)
    queries.append(f"INSERT INTO average_prices (date, av_input_price, av_output_price) VALUES (NOW(), {average_prices['av_input_price']}, {average_prices['av_output_price']})")
    return queries

def create_tables_query(data):
    queries = []
    for key, value in data.items():
        query = f"CREATE TABLE IF NOT EXISTS {clean_column_name(key)} (date DATETIME, "
        for operator in value.keys():
            query += f"{clean_column_name(operator)} VARCHAR(255), "
        query = query.rstrip(", ")
        query += ")"
        queries.append(query)
    queries.append("CREATE TABLE IF NOT EXISTS average_prices (date DATETIME, av_input_price FLOAT, av_output_price FLOAT)")
    return queries

def save_data(data, average_prices):
    cursor = connection.cursor()
    table_queries = create_tables_query(data)
    for query in table_queries:
        cursor.execute(query)
    data_queries = create_data_queries(data, average_prices)
    for query in data_queries:
        cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

def select_data(data):
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='parser',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        date = datetime.strptime(data, '%Y-%m-%d')
        date_start = date.strftime('%Y-%m-%d 00:00:00')
        date_end = date.strftime('%Y-%m-%d 23:59:59')
        result = {}
        for table in tables:
            table_name = table['Tables_in_parser']
            if table_name == 'average_prices':
                continue
            query = f"""
                SELECT * FROM {table_name}
                WHERE date >= '{date_start}' AND date <= '{date_end}'
                ORDER BY date DESC
                LIMIT 1
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                for key, value in row.items():
                    if isinstance(value, datetime):
                        row[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            result[table_name] = rows
        
        cursor.close()
        connection.close()
    except Exception as e:
        result = {"error": str(e)}
    return result

def select_avg():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='parser',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM average_prices")
        result = cursor.fetchall()
        return result
    except Exception as e:
        return {"error": str(e)}
