from . import socketio_client, flask_app
from app.models import Manager, db
import random
import pdb

def test_join_game(socketio_client):
    """
    Test that a user can join a game and that the join-game event is emitted correctly.
    """
    game_id = "Lq3z"
    socketio_client.emit('join-game', {'game-id': game_id})
    received = socketio_client.get_received('/')
    
    assert len(received) > 0  
    assert received[0]['name'] == 'join-game'
    assert received[0]['args'][0]['text'] == f'joined game {game_id}'

def test_end_game(socketio_client):
    """
    Test that the game can be ended and the end-game event is emitted correctly.
    """
    game_id = "Gxx0"
    socketio_client.emit('join-game', {'game-id': game_id})
    socketio_client.emit('end-game', {'game-id': game_id})
    received = socketio_client.get_received('/')
    end_game_event = next(event for event in received if event['name'] == 'end-game')
    assert end_game_event['args'][0]['text'] == f'Closing room {game_id}'

def test_create_manager(socketio_client):
    with socketio_client.app.app_context():
        manager_ids_before_event = [tup[0] for tup in db.session.query(Manager.id).all()]
    socketio_client.emit('create-manager', {})
    received = socketio_client.get_received('/')

    assert len(received) > 0
    assert received[0]['name'] == 'create-manager'
    assert 'manager-id' in received[0]['args'][0]

    with socketio_client.app.app_context():
        manager_id = received[0]['args'][0]['manager-id']
        manager = db.session.get(Manager,manager_id)
        assert manager is not None
        assert manager_id not in manager_ids_before_event
        
