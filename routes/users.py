from flask import request, jsonify
from . import users_bp
from db import get_db_connection
from datetime import datetime

@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    line_user_id = data['line_user_id']
    user_id = data['user_id']
    created_at = datetime.now()
    updated_at = datetime.now()

    conn = get_db_connection()
    conn.execute('INSERT INTO Users (line_user_id, user_id, created_at, updated_at) VALUES (?, ?, ?, ?)',
                 (line_user_id, user_id, created_at, updated_at))
    conn.commit()
    conn.close()
    return jsonify({'status': 'User created'}), 201
