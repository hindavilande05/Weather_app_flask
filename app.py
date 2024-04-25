import requests
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    err_msg = ''
    if request.method == 'POST':
        new_city = request.form.get('city')
        if new_city:
            existing_city = City.query.filter_by(name=new_city).first()
            if not existing_city:
                
                
                new_city_obj = City(name=new_city)
                db.session.add(new_city_obj)
                db.session.commit()
                
            else:
                err_msg = 'City already exists in the database!'
                
           
    cities = City.query.all()
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID=076ee81439f414405e6a0a40e9ac5e67"
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city.name)).json()
        print(f'response: {r}')
        if 'main' in r:
            weather = {
                'city': city.name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
            }
            weather_data.append(weather)
        else:
            err_msg = 'City does not exist !'
            print(f"Error getting weather data for {city.name}")
    return render_template('weather.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run()