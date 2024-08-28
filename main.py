import asyncio
from logic import get_data
from datetime import datetime, timedelta
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/date/<string:date>')
def show_date(date):
    return send_from_directory('prices', f'{date}.json')

@app.route('/avg')
def show_avg():
    return send_from_directory('prices', 'average_prices.json')

async def call_function():
    while True:
        now = datetime.now()
        next_run = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        wait_time = (next_run - now).total_seconds()
        await asyncio.sleep(wait_time)
        get_data()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(call_function())
    app.run(host="0.0.0.0")