from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    deadline_date = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Goal id={self.id} user_id={self.user_id} name={self.name} description={self.description} start_date={self.start_date} deadline_date={self.deadline_date}>'

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
def insert_goal(goal_data):
    new_goal = Goal(
        user_id=goal_data['user_id'],
        name=goal_data['name'],
        description=goal_data['description'],
        start_date=goal_data['start_date'],
        deadline_date=goal_data['deadline_date']
    )
    db.session.add(new_goal)
    db.session.commit()

def get_goals():
    return Goal.query.all()

# def get_db():
#     conn = sqlite3.connect('database.db')
#     return conn

if __name__ == "__main__":
    with app.app_context():
        init_db()

