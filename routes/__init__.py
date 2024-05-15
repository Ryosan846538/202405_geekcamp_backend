from flask import Blueprint

# Define Blueprints
users_bp = Blueprint('users', __name__)
groups_bp = Blueprint('groups', __name__)
goals_bp = Blueprint('goals', __name__)
status_bp = Blueprint('status', __name__)

# Import routes to register them
from . import users, groups, goals, status

def register_blueprints(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(groups_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(status_bp)
