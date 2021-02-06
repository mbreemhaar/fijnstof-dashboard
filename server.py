from flask import Flask, render_template, request
from generate_data import mean_data, timestamp, generate_municipality_map

app = Flask(__name__)
app.debug = True

@app.route('/')
def dashboard():
    return render_template('index.html', provinces=mean_data(), timestamp=timestamp())

@app.route('/gemeentekaart/<int:gemeentecode>')
def render_map(gemeentecode):
    return generate_municipality_map(gemeentecode)

@app.route('/sensorkaart/<name>')
def render_sensor_map(name):
    return generate_sensor_map(name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
