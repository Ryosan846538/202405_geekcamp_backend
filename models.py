from db import get_db_connection

def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            line_user_id TEXT PRIMARY KEY,
            user_id TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS "Group" (
            group_id TEXT PRIMARY KEY,
            line_user_id TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (line_user_id) REFERENCES Users(line_user_id)
        )''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Goal (
            goal_id TEXT PRIMARY KEY,
            user_id TEXT,
            description TEXT,
            start_date DATE,
            end_date DATE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(line_user_id)
        )''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Status (
            goal_id TEXT PRIMARY KEY,
            status TEXT,
            FOREIGN KEY (goal_id) REFERENCES Goal(goal_id)
        )''')
    conn.close()
