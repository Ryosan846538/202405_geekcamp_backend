from flask import request, jsonify
from . import groups_bp
from db import get_db_connection
from datetime import datetime

@groups_bp.route('/groups', methods=['POST'])
def create_group():
    data = request.get_json()
    group_id = data['group_id']
    line_user_id = data['line_user_id']
    created_at = datetime.now()
    updated_at = datetime.now()

    conn = get_db_connection()
    conn.execute('INSERT INTO "Group" (group_id, line_user_id, created_at, updated_at) VALUES (?, ?, ?, ?)',
                 (group_id, line_user_id, created_at, updated_at))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Group created'}), 201
