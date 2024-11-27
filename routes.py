from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from models import db, Observation
from schemas import ObservationSchema

bp = Blueprint('api', __name__)
obs_schema = ObservationSchema()
obs_list_schema = ObservationSchema(many=True)

@bp.route('/observations', methods=['POST'])
@jwt_required()
def add_observation():
    data = request.get_json()
    try:
        observation = obs_schema.load(data)
        new_observation = Observation(**observation)
        db.session.add(new_observation)
        db.session.commit()
        return jsonify(obs_schema.dump(new_observation)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/observations', methods=['GET'])
@jwt_required()
def get_observations():
    filters = request.args  # Use query parameters for filtering
    query = Observation.query

    for key, value in filters.items():
        if hasattr(Observation, key):
            query = query.filter(getattr(Observation, key) == value)

    results = query.all()
    return jsonify(obs_list_schema.dump(results)), 200
