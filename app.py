from flask import Flask
from models import init_db
from routes import register_blueprints

app = Flask(__name__)

# Register the blueprints
register_blueprints(app)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
