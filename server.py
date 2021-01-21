from flask import Flask, render_template, request
import pandas as pd
import os

from generate_data import mean_data, timestamp, nearest_sensor_data

app = Flask(__name__)
app.debug = True

@app.route('/')
def dashboard():
    #nearest_sensor = nearest_sensor_data(request.remote_addr)
    nearest_sensor = nearest_sensor_data('217.21.206.119')
    return render_template('index.html', provinces=mean_data(), timestamp=timestamp(), nearest_sensor=nearest_sensor)

if __name__ == '__main__':
    app.run()
