#!/usr/bin/python3

from flask import Flask, Response, render_template, stream_with_context
from sense_hat import SenseHat

import json
import random
import time
from datetime import datetime



app = Flask(__name__)

random.seed()  # Initialize the random number generator
sense = SenseHat()


def get_json_temperature():
    t = round(sense.get_temperature(),4)
    return {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': t}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            #json_data = json.dumps(
            #    {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            json_data = json.dumps( get_json_temperature())
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


if __name__ == '__main__':
    app.run(host="192.168.1.146", port=8080, debug=True, threaded=True)
