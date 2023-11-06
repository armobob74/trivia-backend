from flask import Flask
from flask_socketio import SocketIO
from .models import db
from flask_cors import CORS

socketio = SocketIO()

def create_app(debug=False, test_mode=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'rijgsiejfies'
    app.config['FRONTEND_URL'] = 'http://localhost:5173'
    if test_mode:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    with app.app_context():
        db.create_all()

    CORS(app, supports_credentials=True,origins=[app.config['FRONTEND_URL']])
    return app
