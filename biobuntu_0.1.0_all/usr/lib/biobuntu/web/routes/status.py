from flask import Blueprint, jsonify

status_bp = Blueprint('status', __name__)

@status_bp.route('/status')
def get_status():
    return jsonify({
        'status': 'online',
        'version': '0.1.0',
        'uptime': 'N/A'
    })