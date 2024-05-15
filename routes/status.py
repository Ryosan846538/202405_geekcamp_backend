from flask import request, jsonify
from . import status_bp
from db import get_db_connection

@status_bp.route('/status', methods=['POST'])
def create_status():
    data = request.get_json()
    goal_id = data['goal_id']
    status = data['status']

    conn = get_db_connection()
    conn.execute('INSERT INTO Status (goal_id, status) VALUES (?, ?)',
                 (goal_id, status))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Status created'}), 201
