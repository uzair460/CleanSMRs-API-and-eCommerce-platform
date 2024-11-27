from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime

# Initialize the Flask app and the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cleansmrs.db'  # Unified database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Observation model (part of cleansmrs.db)
class Observation(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    time_zone_offset = db.Column(db.String(10), nullable=False)
    coordinates = db.Column(db.String(50), nullable=False)
    temperature_water = db.Column(db.Float, nullable=True)
    temperature_air = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    wind_speed = db.Column(db.Float, nullable=True)
    wind_direction = db.Column(db.Float, nullable=True)
    precipitation = db.Column(db.Float, nullable=True)
    haze = db.Column(db.Float, nullable=True)
    becquerel = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Observation {self.id}>"

    @staticmethod
    def create(date, time, time_zone_offset, coordinates, temperature_water=None, temperature_air=None,
               humidity=None, wind_speed=None, wind_direction=None, precipitation=None, haze=None, becquerel=None, notes=None):
        observation = Observation(
            date=date,
            time=time,
            time_zone_offset=time_zone_offset,
            coordinates=coordinates,
            temperature_water=temperature_water,
            temperature_air=temperature_air,
            humidity=humidity,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            precipitation=precipitation,
            haze=haze,
            becquerel=becquerel,
            notes=notes
        )
        db.session.add(observation)
        db.session.commit()
        return observation

# Create tables in the cleansmrs.db database
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    return "Welcome to the CleanSMRS API!"

# API endpoint to create a new observation
@app.route('/observations', methods=['POST'])
def create_observation():
    data = request.get_json()  # Get the JSON data from the request
    
    # Extract data from the JSON body
    date = data.get('date')
    time = data.get('time')
    time_zone_offset = data.get('time_zone_offset')
    coordinates = data.get('coordinates')
    temperature_water = data.get('temperature_water')
    temperature_air = data.get('temperature_air')
    humidity = data.get('humidity')
    wind_speed = data.get('wind_speed')
    wind_direction = data.get('wind_direction')
    precipitation = data.get('precipitation')
    haze = data.get('haze')
    becquerel = data.get('becquerel')
    notes = data.get('notes')

    try:
        # Convert date and time from strings to Python objects
        date = datetime.strptime(date, '%Y-%m-%d').date()
        time = datetime.strptime(time, '%H:%M:%S').time()

        # Call the create method on the Observation model
        observation = Observation.create(
            date=date,
            time=time,
            time_zone_offset=time_zone_offset,
            coordinates=coordinates,
            temperature_water=temperature_water,
            temperature_air=temperature_air,
            humidity=humidity,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            precipitation=precipitation,
            haze=haze,
            becquerel=becquerel,
            notes=notes
        )
        return jsonify({"message": "Observation created successfully", "data": observation.id}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to create observation: {str(e)}"}), 400

# API endpoint to get all observations
@app.route('/observations', methods=['GET'])
def get_observations():
    observations = Observation.query.all()  # Fetch all observations from the database
    # Serialize observations (convert them into JSON)
    observations_list = []
    for observation in observations:
        observations_list.append({
            "id": observation.id,
            "date": observation.date.strftime('%Y-%m-%d'),
            "time": observation.time.strftime('%H:%M:%S'),
            "time_zone_offset": observation.time_zone_offset,
            "coordinates": observation.coordinates,
            "temperature_water": observation.temperature_water,
            "temperature_air": observation.temperature_air,
            "humidity": observation.humidity,
            "wind_speed": observation.wind_speed,
            "wind_direction": observation.wind_direction,
            "precipitation": observation.precipitation,
            "haze": observation.haze,
            "becquerel": observation.becquerel,
            "notes": observation.notes,
            "created": observation.created.strftime('%Y-%m-%d %H:%M:%S'),
            "updated": observation.updated.strftime('%Y-%m-%d %H:%M:%S') if observation.updated else None,
            "deleted": observation.deleted.strftime('%Y-%m-%d %H:%M:%S') if observation.deleted else None
        })
    
    return jsonify(observations_list), 200

# API endpoint to delete an observation by its ID
@app.route('/observations/<string:id>', methods=['DELETE'])
def delete_observation(id):
    observation = Observation.query.get(id)
    if observation is None:
        return jsonify({"error": "Observation not found"}), 404

    db.session.delete(observation)
    db.session.commit()

    return jsonify({"message": f"Observation {id} deleted successfully"}), 200

# API endpoint to get an observation by its ID
@app.route('/observations/<string:id>', methods=['GET'])
def get_observation(id):
    observation = Observation.query.filter_by(id=id).first()
    
    if observation is None:
        return jsonify({"error": "Observation not found"}), 404

    # Serialize observation to return it as JSON
    observation_data = {
        "id": observation.id,
        "date": observation.date.strftime('%Y-%m-%d'),
        "time": observation.time.strftime('%H:%M:%S'),
        "time_zone_offset": observation.time_zone_offset,
        "coordinates": observation.coordinates,
        "temperature_water": observation.temperature_water,
        "temperature_air": observation.temperature_air,
        "humidity": observation.humidity,
        "wind_speed": observation.wind_speed,
        "wind_direction": observation.wind_direction,
        "precipitation": observation.precipitation,
        "haze": observation.haze,
        "becquerel": observation.becquerel,
        "notes": observation.notes,
        "created": observation.created.strftime('%Y-%m-%d %H:%M:%S'),
        "updated": observation.updated.strftime('%Y-%m-%d %H:%M:%S') if observation.updated else None,
        "deleted": observation.deleted.strftime('%Y-%m-%d %H:%M:%S') if observation.deleted else None
    }

    return jsonify(observation_data), 200

# API endpoint to update an observation by its ID
@app.route('/observations/<string:id>', methods=['PUT'])
def update_observation(id):
    observation = Observation.query.get(id)
    if observation is None:
        return jsonify({"error": "Observation not found"}), 404

    data = request.get_json()  # Get the updated data from the request

    # Update the fields of the observation if provided
    if 'date' in data:
        observation.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    if 'time' in data:
        observation.time = datetime.strptime(data['time'], '%H:%M:%S').time()
    if 'time_zone_offset' in data:
        observation.time_zone_offset = data['time_zone_offset']
    if 'coordinates' in data:
        observation.coordinates = data['coordinates']
    if 'temperature_water' in data:
        observation.temperature_water = data.get('temperature_water')
    if 'temperature_air' in data:
        observation.temperature_air = data.get('temperature_air')
    if 'humidity' in data:
        observation.humidity = data.get('humidity')
    if 'wind_speed' in data:
        observation.wind_speed = data.get('wind_speed')
    if 'wind_direction' in data:
        observation.wind_direction = data.get('wind_direction')
    if 'precipitation' in data:
        observation.precipitation = data.get('precipitation')
    if 'haze' in data:
        observation.haze = data.get('haze')
    if 'becquerel' in data:
        observation.becquerel = data.get('becquerel')
    if 'notes' in data:
        observation.notes = data.get('notes')

    # Commit the changes to the database
    db.session.commit()

    return jsonify({"message": "Observation updated successfully", "data": observation.id}), 200

if __name__ == '__main__':
    create_tables()  # Create the tables explicitly within the app context
    app.run(debug=True)




