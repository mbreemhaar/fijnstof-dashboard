from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    provinces = [{'name': 'Drenthe', 'municipalities': [
        {'name': 'Aa en Hunze', 'pm10': 20, 'pm25': 10, 'temp': 2, 'rh': 86, 'n_sensors': 16},
        {'name': 'Aa en Hunze', 'pm10': 20, 'pm25': 10, 'temp': 2, 'rh': 86, 'n_sensors': 16},
        {'name': 'Aa en Hunze', 'pm10': 20, 'pm25': 10, 'temp': 2, 'rh': 86, 'n_sensors': 16},
        {'name': 'Aa en Hunze', 'pm10': 20, 'pm25': 10, 'temp': 2, 'rh': 86, 'n_sensors': 16},
        {'name': 'Aa en Hunze', 'pm10': 20, 'pm25': 10, 'temp': 2, 'rh': 86, 'n_sensors': 16},
        {'name': 'Aa en Hunze', 'pm10': 20, 'pm25': 10, 'temp': 2, 'rh': 86, 'n_sensors': 16}],},
        {'name': 'Groningen', 'municipalities': [
        {'name': 'Aa en Hunze', 'pm10': 20, 'pm25': 10, 'temp': 2, 'rh': 86, 'n_sensors': 16},
        {'name': 'Aa en Hunze', 'pm10': 20, 'pm25': 10, 'temp': 2, 'rh': 86, 'n_sensors': 16},
        {'name': 'Aa en Hunze', 'pm10': 20, 'pm25': 10, 'temp': 2, 'rh': 86, 'n_sensors': 16},
        {'name': 'Aa en Hunze', 'pm10': 20, 'pm25': 10, 'temp': 2, 'rh': 86, 'n_sensors': 16},
        {'name': 'Aa en Hunze', 'pm10': 10, 'pm25': 10, 'temp': 2, 'rh': 86, 'n_sensors': 16},
        {'name': 'Aa en Hunze', 'pm10': 20, 'pm25': 10, 'temp': 2, 'rh': 86, 'n_sensors': 16}],},
        ]
    return render_template('index.html', provinces=provinces)

if __name__ == '__main__':
    app.run()
