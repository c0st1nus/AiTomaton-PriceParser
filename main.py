# -*- coding: utf-8 -*-
import asyncio
import logic
from datetime import datetime
from flask import Flask, send_from_directory, abort
from threading import Thread
import os
import handler
from flask_cors import CORS, cross_origin

app = Flask(__name__)

@app.route('/date/<string:date>')
@cross_origin()
def show_date(date):    
    return handler.select_data(date)

@app.route('/log')
def show_log():
    return send_from_directory(os.path.dirname(__file__), 'log.txt')

@app.route('/avg/')
@cross_origin()
def show_avg():
    return handler.select_avg()

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
    app.run(host="0.0.0.0", port=3006)
