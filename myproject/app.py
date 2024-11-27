from flask import Flask, jsonify, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the model
class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))  # YYYY-MM-DD
    time = db.Column(db.String(8))   # hh:mm:ss
    timezone_offset = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    water_temperature = db.Column(db.Float)
    ambient_air_temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    wind_direction = db.Column(db.Float)
    precipitation = db.Column(db.Float)
    haze = db.Column(db.Float)
    becquerel = db.Column(db.Float)

@app.route('/')
def index():
    return render_template('index.html') 

# CREATE: Add new data
@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.get_json()
    if not new_data:
        abort(400, description="No data provided")
    
    weather = WeatherData(
        date=new_data['date'],
        time=new_data['time'],
        timezone_offset=new_data['timezone_offset'],
        latitude=new_data['latitude'],
        longitude=new_data['longitude'],
        water_temperature=new_data['water_temperature'],
        ambient_air_temperature=new_data['ambient_air_temperature'],
        humidity=new_data['humidity'],
        wind_speed=new_data['wind_speed'],
        wind_direction=new_data['wind_direction'],
        precipitation=new_data['precipitation'],
        haze=new_data['haze'],
        becquerel=new_data['becquerel']
    )
    db.session.add(weather)
    db.session.commit()
    return jsonify({'message': 'Data added successfully'}), 201

# READ: Get all data
@app.route('/data', methods=['GET'])
def get_data():
    records = WeatherData.query.all()
    data = [{
        "id": r.id,
        "date": r.date,
        "time": r.time,
        "timezone_offset": r.timezone_offset,
        "latitude": r.latitude,
        "longitude": r.longitude,
        "water_temperature": r.water_temperature,
        "ambient_air_temperature": r.ambient_air_temperature,
        "humidity": r.humidity,
        "wind_speed": r.wind_speed,
        "wind_direction": r.wind_direction,
        "precipitation": r.precipitation,
        "haze": r.haze,
        "becquerel": r.becquerel
    } for r in records]
    return jsonify(data)

# READ: Get a single record by ID
@app.route('/data/<int:id>', methods=['GET'])
def get_single_data(id):
    weather = WeatherData.query.get_or_404(id)
    data = {
        "id": weather.id,
        "date": weather.date,
        "time": weather.time,
        "timezone_offset": weather.timezone_offset,
        "latitude": weather.latitude,
        "longitude": weather.longitude,
        "water_temperature": weather.water_temperature,
        "ambient_air_temperature": weather.ambient_air_temperature,
        "humidity": weather.humidity,
        "wind_speed": weather.wind_speed,
        "wind_direction": weather.wind_direction,
        "precipitation": weather.precipitation,
        "haze": weather.haze,
        "becquerel": weather.becquerel
    }
    return jsonify(data)

# UPDATE: Update an existing record by ID
@app.route('/data/<int:id>', methods=['PUT'])
def update_data(id):
    weather = WeatherData.query.get_or_404(id)
    updated_data = request.get_json()
    
    weather.date = updated_data.get('date', weather.date)
    weather.time = updated_data.get('time', weather.time)
    weather.timezone_offset = updated_data.get('timezone_offset', weather.timezone_offset)
    weather.latitude = updated_data.get('latitude', weather.latitude)
    weather.longitude = updated_data.get('longitude', weather.longitude)
    weather.water_temperature = updated_data.get('water_temperature', weather.water_temperature)
    weather.ambient_air_temperature = updated_data.get('ambient_air_temperature', weather.ambient_air_temperature)
    weather.humidity = updated_data.get('humidity', weather.humidity)
    weather.wind_speed = updated_data.get('wind_speed', weather.wind_speed)
    weather.wind_direction = updated_data.get('wind_direction', weather.wind_direction)
    weather.precipitation = updated_data.get('precipitation', weather.precipitation)
    weather.haze = updated_data.get('haze', weather.haze)
    weather.becquerel = updated_data.get('becquerel', weather.becquerel)

    db.session.commit()
    return jsonify({'message': 'Data updated successfully'}), 200

# DELETE: Delete a record by ID
@app.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    weather = WeatherData.query.get_or_404(id)
    db.session.delete(weather)
    db.session.commit()
    return jsonify({'message': 'Data deleted successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
