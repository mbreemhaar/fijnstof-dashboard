from flask import Flask, render_template
import pandas as pd
import os

from generate_data import generate_data

app = Flask(__name__)
app.debug = True

@app.route('/')
def dashboard():
    return render_template('index.html', provinces=generate_data())

if __name__ == '__main__':
    app.run()
