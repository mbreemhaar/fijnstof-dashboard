from flask import Flask, render_template
import pandas as pd
import os

from generate_data import mean_data, timestamp

app = Flask(__name__)
app.debug = True

@app.route('/')
def dashboard():
    return render_template('index.html', provinces=mean_data(), timestamp=timestamp())

if __name__ == '__main__':
    app.run()
