from . import socketio_client, flask_app
from app.models import Manager, db, Game
import random
import pdb

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
len_game_id = 4

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
    This event just closes the room -- it does not remove game from database
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
        
def test_create_game(socketio_client):
    with socketio_client.app.app_context():
        ids_before_event = [tup[0] for tup in db.session.query(Game.id).all()]
    game_id = 'AAAA'
    while game_id in ids_before_event:
        game_id = ''.join([random.choice(chars) for _ in range(len_game_id)])
    socketio_client.emit('create-game', {'manager-id':1,'game-id':game_id})
    with socketio_client.app.app_context():
        game = db.session.get(Game,game_id)
        assert game is not None
        assert game_id not in ids_before_event
        assert game.manager is not None
        assert game in game.manager.games
