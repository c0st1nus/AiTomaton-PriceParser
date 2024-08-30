import asyncio
from logic import get_data
from datetime import datetime
from flask import Flask, send_from_directory
from threading import Thread
import os

app = Flask(__name__)

@app.route('/date/<string:date>')
def show_date(date):
    directory = os.path.join('prices', date)
    
    if not os.path.exists(directory):
        abort(404, description="Directory not found")
    
    files = os.listdir(directory)
    if not files:
        abort(404, description="No files found in directory")
    
    files = [os.path.join(directory, f) for f in files]
    latest_file = max(files, key=os.path.getctime)
    print(latest_file)
    
    return send_from_directory(directory, os.path.basename(latest_file))

@app.route('/avg')
def show_avg():
    return send_from_directory('', 'average_prices.json')

async def call_function():
    while True:
        get_data()
        now = datetime.now()
        print('Before:', now)
        await asyncio.sleep(60)
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
    app.run(host="0.0.0.0", port="8080")