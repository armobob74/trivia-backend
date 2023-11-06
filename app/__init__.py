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
    FRONTEND_URL = 'http://localhost:5173'
    app.config['CORS_ALLOWED_ORIGINS'] = [FRONTEND_URL]
    if test_mode:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    CORS(app, supports_credentials=True,origins=app.config['CORS_ALLOWED_ORIGINS'])
    socketio.init_app(app, cors_allowed_origins=app.config['CORS_ALLOWED_ORIGINS'])
    with app.app_context():
        db.create_all()
    return app
