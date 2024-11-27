# get.py
from flask import Flask, jsonify, request, abort
from models import db, Observation
from schemas import ObservationSchema  # Assuming you have a schema for serializing data

app = Flask(__name__)

# Route to get all observations (GET request)
@app.route('/api/observations', methods=['GET'])
def get_observations():
    observations = Observation.query.all()  # Fetch all observations from the database
    schema = ObservationSchema(many=True)  # Use schema to serialize the data
    return jsonify(schema.dump(observations)), 200

# Route to get a specific observation by ID (GET request)
@app.route('/api/observations/<string:id>', methods=['GET'])  # Use string for UUID
def get_observation(id):
    observation = Observation.query.get(id)  # Find observation by ID
    if observation is None:
        return jsonify({"error": "Observation not found"}), 404  # If not found, return error
    schema = ObservationSchema()  # Use schema to serialize the data
    return jsonify(schema.dump(observation)), 200

# Route to create a new observation (POST request)
@app.route('/api/observations', methods=['POST'])
def create_observation():
    data = request.get_json()  # Get the data sent in the request body
    
    # Extract necessary fields from the JSON body
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

    # Validate input
    if not date or not time or not coordinates:  # You can add more validation as needed
        return jsonify({"error": "Missing required fields"}), 400
    
    # Create a new observation record
    try:
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
        schema = ObservationSchema()  # Serialize the created observation
        return jsonify({"message": "Observation created successfully", "data": schema.dump(observation)}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to create observation: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True)
