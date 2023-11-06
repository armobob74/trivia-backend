import pytest
from app import create_app, socketio

@pytest.fixture
def flask_app():
    app = create_app(test_mode=True)
    return app

@pytest.fixture
def socketio_client(flask_app):
    # Use the test_client provided by Flask-SocketIO
    return socketio.test_client(flask_app, namespace='/')

