from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4

# Initialize the Flask app
app = Flask(__name__)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///observations.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)


# Define the Observation model
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


# Create the tables in the database
@app.before_first_request
def create_tables():
    db.create_all()


# Route to add a new observation
@app.route('/api/observations', methods=['POST'])
def add_observation():
    # Get the JSON data from the request
    data = request.get_json()

    # Validate required fields
    required_fields = ['date', 'time', 'time_zone_offset', 'coordinates']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required."}), 400

    try:
        # Create a new Observation object
        observation = Observation(
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            time=datetime.strptime(data['time'], '%H:%M:%S').time(),
            time_zone_offset=data['time_zone_offset'],
            coordinates=data['coordinates'],
            temperature_water=data.get('temperature_water'),
            temperature_air=data.get('temperature_air'),
            humidity=data.get('humidity'),
            wind_speed=data.get('wind_speed'),
            wind_direction=data.get('wind_direction'),
            precipitation=data.get('precipitation'),
            haze=data.get('haze'),
            becquerel=data.get('becquerel'),
            notes=data.get('notes')
        )

        # Add the observation to the database session and commit
        db.session.add(observation)
        db.session.commit()

        # Return the newly created observation
        return jsonify({
            "message": "Observation created successfully!",
            "observation": {
                "id": observation.id,
                "date": observation.date.isoformat(),
                "time": observation.time.isoformat(),
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
                "created": observation.created.isoformat(),
                "updated": observation.updated.isoformat() if observation.updated else None
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
