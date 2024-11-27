from flask import Flask, request, jsonify
from models import db, Observation
from schemas import ObservationSchema

app = Flask(__name__)

# Configuration for database (same as in your main app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///observations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# Route to create a new observation
@app.route('/api/observations', methods=['POST'])
def create_observation():
    # Get the data sent with the POST request
    data = request.get_json()
    schema = ObservationSchema()

    # Validate and deserialize the data
    try:
        # This will validate and transform the incoming JSON data
        observation_data = schema.load(data)
    except Exception as e:
        # If validation fails, return an error
        return jsonify({"error": str(e)}), 400

    # Create and save the new observation
    new_observation = Observation(
        date=observation_data['date'],
        time=observation_data['time'],
        time_zone_offset=observation_data['time_zone_offset'],
        coordinates=observation_data['coordinates'],
        temperature_water=observation_data.get('temperature_water'),  # Optional fields
        temperature_air=observation_data.get('temperature_air'),
        humidity=observation_data.get('humidity'),
        wind_speed=observation_data.get('wind_speed'),
        wind_direction=observation_data.get('wind_direction'),
        precipitation=observation_data.get('precipitation'),
        haze=observation_data.get('haze'),
        becquerel=observation_data.get('becquerel'),
        notes=observation_data.get('notes')
    )

    db.session.add(new_observation)  # Add the new observation to the database session
    db.session.commit()  # Commit the transaction to the database

    # Return the created observation as a JSON response
    return jsonify(schema.dump(new_observation)), 201  # Return the created data with a 201 status


if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)
