from flask import Flask
from models import init_db
from routes import register_blueprints
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Register the blueprints
register_blueprints(app)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
