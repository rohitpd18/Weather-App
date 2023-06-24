from flask import Flask, render_template, request
from datetime import datetime
import requests

app = Flask(__name__)

API_KEY = 'c9d3180a526ee27861dc136b4508ff4f'

# home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather_data(city)
        if weather_data:
            return render_template('weather.html', weather_data=weather_data)
        else:
            error_msg = 'Unable to fetch weather data for the specified city. Please try again.'
            return render_template('index.html', error_msg=error_msg)
    return render_template('index.html')

# weather by location
@app.route('/weather_by_location', methods=['POST'])
def weather_by_location():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    city = get_city_from_coordinates(latitude, longitude)
    weather_data = get_weather_data(city)
    if weather_data:
        return render_template('weather.html', weather_data=weather_data)
    else:
        error_msg = 'Unable to fetch weather data for your location. Please try again.'
        return render_template('index.html', error_msg=error_msg)
    
# getting weather data by city name
def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    if data['cod'] == '404':
        return None

    location = data['coord']['lon'], data['coord']['lat']
    sunrise = data['sys']['sunrise']
    sunset = data['sys']['sunset']
    main_weather = data['weather'][0]['main']
    description = data['weather'][0]['description']
    temperature = data['main']['temp']
    feels_like = data['main']['feels_like']
    tempC=round(temperature+273.15,2)
    feelC=round(feels_like+273.15,2)
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    visibility = data['visibility']
    cloudiness = data['clouds']['all']
    rain = data.get('rain', {}).get('1h', 0)
    snow = data.get('snow', {}).get('1h', 0)
    icon = data['weather'][0]['icon']  # Extract the weather icon code


    # Convert sunrise and sunset timestamps to human-readable format and in UTC
    sunrise_time =  sunrise_time = datetime.utcfromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S')
    sunset_time = datetime.utcfromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S')

    print(feelC, tempC)
    weather_data = {
        'city': data['name'],
        'country': data['sys']['country'],
        'longitude': location[0],
        'latitude': location[1],
        'sunrise': sunrise_time + " UTC",
        'sunset': sunset_time + " UTC",
        'main_weather': main_weather,
        'description': description,
        'temperature': temperature,
        'feels_like': feels_like,
        'tempC':tempC,
        'feelC':feelC,
        'pressure': pressure,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'visibility': visibility,
        'cloudiness': cloudiness,
        'rain': rain,
        'snow': snow,
        'icon': icon
    }

    return weather_data

# getting city name from coordinates
def get_city_from_coordinates(latitude, longitude):
    url = f'http://api.openweathermap.org/geo/1.0/reverse?lat={latitude}&lon={longitude}&limit=1&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if data:
        return data[0]['name']
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True,port=5501)
