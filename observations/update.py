# update.py
from flask import Flask, request, jsonify
from models import db, Observation
from schemas import ObservationSchema

app = Flask(__name__)

@app.route('/api/observations/<int:id>', methods=['PUT'])
def update_observation(id):
    observation = Observation.query.get(id)
    if observation is None:
        return jsonify({"error": "Observation not found"}), 404

    data = request.get_json()
    schema = ObservationSchema()

    # Validate and load the incoming data
    try:
        updated_data = schema.load(data, partial=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Update the observation fields
    observation.title = updated_data['title']
    observation.description = updated_data['description']

    db.session.commit()

    return jsonify(schema.dump(observation)), 200

if __name__ == '__main__':
    app.run(debug=True)
