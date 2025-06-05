from flask import Blueprint, request, jsonify
from app.services.cocomo import calculate_cocomo

estimation_bp = Blueprint('estimation', __name__)

@estimation_bp.route('/estimate/cocomo', methods=['POST'])
def cocomo():
    data = request.get_json()
    kloc = float(data['kloc'])
    mode = data.get('mode', 'organic')
    result = calculate_cocomo(kloc, mode)
    return jsonify(result)
