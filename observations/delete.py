from flask import Flask, jsonify, abort
from models import db, Observation

app = Flask(__name__)

# API endpoint to delete an observation by ID
@app.route('/observations/<observation_id>', methods=['DELETE'])
def delete_observation(observation_id):
    observation = Observation.query.get(observation_id)
    
    if observation is None:
        abort(404, description="Observation not found")
    
    # Delete the observation
    db.session.delete(observation)
    db.session.commit()

    return jsonify({"message": f"Observation {observation_id} deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
