# patch.py
from flask import Flask, request, jsonify
from models import db, Observation
from schemas import ObservationSchema

app = Flask(__name__)

@app.route('/api/observations/<int:id>', methods=['PATCH'])
def patch_observation(id):
    observation = Observation.query.get(id)
    if observation is None:
        return jsonify({"error": "Observation not found"}), 404

    data = request.get_json()
    schema = ObservationSchema(partial=True)

    # Validate and load the partial data
    try:
        partial_data = schema.load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Update only the fields that are provided
    if 'title' in partial_data:
        observation.title = partial_data['title']
    if 'description' in partial_data:
        observation.description = partial_data['description']

    db.session.commit()

    return jsonify(schema.dump(observation)), 200

if __name__ == '__main__':
    app.run(debug=True)
