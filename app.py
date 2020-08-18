import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__) 
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET','POST']) 
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')
        if new_city: 
            new_city_obj = City(name=new_city) 
            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=7c0802a3ab9e59e9d479af1da0b549d6'

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()
        weather = {
            'city' : city.name, 
            'temp' : r['main']['temp'], 
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon']
        }

        weather_data.append(weather)
        
    return render_template('weather.html', weather_data=weather_data) 

    # {
    # 'coord': {'lon': -118.24, 'lat': 34.05}, 
    # 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 
    # 'base': 'stations', 
    # 'main': {'temp': 92.1, 'feels_like': 97.61, 'temp_min': 78.8, 'temp_max': 99, 'pressure': 1012, 'humidity': 48}, 
    # 'visibility': 10000, 
    # 'wind': {'speed': 3.36, 'deg': 0}, 
    # 'clouds': {'all': 1}, 
    # 'dt': 1597702345, 
    # 'sys': {'type': 1, 'id': 3694, 'country': 'US', 'sunrise': 1597670189, 'sunset': 1597718256}, 
    # 'timezone': -25200, 'id': 5368361, 'name': 'Los Angeles', 'cod': 200
    # }

