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
    start = db.Column(db.String(20), nullable=False)
    deadline = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Goal id={self.id} user_id={self.user_id} name={self.name} description={self.description} start={self.start} deadline={self.deadline}>'

def init_db():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        init_db()
