from . import flask_app, socketio_client 
import pdb

def test_join_game(flask_app, socketio_client):
    """
    Test that a user can join a game and that the join-game event is emitted correctly.
    """
    game_id = "1234"
    socketio_client.emit('join-game', {'game-id': game_id})
    received = socketio_client.get_received('/')
    
    assert len(received) > 0  
    assert received[0]['name'] == 'join-game'
    assert received[0]['args'][0]['text'] == f'joined game {game_id}'

def test_end_game(flask_app, socketio_client):
    """
    Test that the game can be ended and the end-game event is emitted correctly.
    """
    game_id = "1234"
    # First, join the game to create the room
    socketio_client.emit('join-game', {'game-id': game_id})
    socketio_client.emit('end-game', {'game-id': game_id})
    received = socketio_client.get_received('/')
    # Depending on how your actual event handling code is set up, you might need to filter received events
    end_game_event = next(event for event in received if event['name'] == 'end-game')
    assert end_game_event['args'][0]['text'] == f'Closing room {game_id}'
    # Here you would need to check if the room is indeed closed, but that functionality isn't provided by the test client

