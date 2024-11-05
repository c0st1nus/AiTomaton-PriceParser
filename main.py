import asyncio
import dumpHandler
import schedule
import logic
from datetime import datetime
from flask import Flask, send_file, abort, send_from_directory
from threading import Thread
import os
import handler
from flask_cors import CORS, cross_origin
from table import generate_table
from dumpHandler import create_dump

# -*- coding: utf-8 -*-

app = Flask(__name__)

@app.route('/get_table/<string:date>')
@cross_origin()
def get_table(date):
    try:
        output = generate_table(date)
        return send_file(output, as_attachment=True, download_name=f"selected_rows_{date.replace(':', '-')}.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        print(f"Error generating table: {e}")
        abort(500, description="Error generating table")

@app.route('/date/<string:date>')
@cross_origin()
def show_date(date):    
    return handler.select_data(date)

@app.route('/bench/<string:date>')
@cross_origin()
def show_bench(date):    
    return handler.bench(date)

@app.route('/log')
def show_log():
    return send_from_directory(os.path.dirname(__file__), 'log.txt')

@app.route('/avg/')
@cross_origin()
def show_avg():
    return handler.select_avg()

async def daily_backup():
    while True:
        dumpHandler.create_dump(datetime.now().strftime("%Y-%m-%d"))
        print(f"Backup created: {datetime.now()}")
        await asyncio.sleep(86400) 


async def call_function():
    while True:
        logic.get_data()
        now = datetime.now()
        print('Before:', now)
        await asyncio.sleep(14400)
        now = datetime.now()
        print('After:', now)

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == '__main__':
    new_loop = asyncio.new_event_loop()
    t = Thread(target=start_loop, args=(new_loop,))
    t.start()
    
    new_loop.call_soon_threadsafe(new_loop.create_task, call_function())
    new_loop.call_soon_threadsafe(new_loop.create_task, daily_backup())
    
    app.run(host="0.0.0.0", port=3006)