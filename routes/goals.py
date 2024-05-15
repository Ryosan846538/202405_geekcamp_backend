from flask import request, jsonify
from . import goals_bp
from db import get_db_connection
from datetime import datetime

@goals_bp.route('/goals', methods=['POST'])
def create_goal():
    data = request.get_json()
    goal_id = data['goal_id']
    user_id = data['user_id']
    description = data['description']
    start_date = data['start_date']
    end_date = data['end_date']
    created_at = datetime.now()
    updated_at = datetime.now()

    conn = get_db_connection()
    conn.execute('INSERT INTO Goal (goal_id, user_id, description, start_date, end_date, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (goal_id, user_id, description, start_date, end_date, created_at, updated_at))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Goal created'}), 201
