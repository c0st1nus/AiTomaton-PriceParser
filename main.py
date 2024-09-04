import asyncio
import logic
from datetime import datetime
from flask import Flask, send_from_directory, abort
from threading import Thread
import os
import handler

app = Flask(__name__)

@app.route('/date/<string:date>')
def show_date(date):    
    return handler.select_data(date)

@app.route('/avg')
def show_avg():
    return handler.select_avg()

async def call_function():
    while True:
        logic.get_data()
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
    app.run(host="0.0.0.0", port="8080")    import asyncio
    import logic
    from datetime import datetime
    from flask import Flask, send_from_directory, abort
    from flask_cors import CORS
    from threading import Thread
    import os
    import handler
    
    app = Flask(__name__)
    CORS(app)  # Добавьте эту строку для включения CORS
    
    @app.route('/date/<string:date>')
    def show_date(date):    
        return handler.select_data(date)
    
    @app.route('/avg')
    def show_avg():
        return handler.select_avg()
    
    async def call_function():
        while True:
            logic.get_data()
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