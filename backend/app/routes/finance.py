from flask import Blueprint, request, jsonify
from app.services.npv import calculate_npv

finance_bp = Blueprint('finance', __name__)

@finance_bp.route('/npv', methods=['POST'])
def npv():
    data = request.get_json()
    cash_flows = data.get('cash_flows', [])
    rate = float(data.get('discount_rate', 0.1))

    if not isinstance(cash_flows, list) or not cash_flows:
        return jsonify({'error': 'cash_flows must be a non-empty list'}), 400

    try:
        result = calculate_npv(cash_flows, rate)
        return jsonify({'npv': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
