import pymysql
import json

config = json.load(open('config.json'))

connection = pymysql.connect(
    host = "localhost",
    user='root',
    password='root',
    database='parser',
    port=6033
)

try:
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        for table in tables:
            cursor.execute(f"DELETE FROM `{table}` ORDER BY date DESC LIMIT 1")
    connection.commit()
finally:
    connection.close()