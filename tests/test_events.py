from . import socketio_client, flask_app
import random

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

def test_create_item_demo(socketio_client, flask_app):
    """
    test item creation
    """

    #choose a random word that will pretty much definitely not exist in the db table
    choices = 'abcdefghijklmnopqrstuvwxyz' +  'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + '01234567890'
    word = ''.join([random.choice(choices) for _ in range(64)]) 
    socketio_client.emit('create-item-demo',{'demo-model':{'word':word}} )

    recieved = socketio_client.get_received('/')
    assert len(recieved) > 0

    text = recieved[0]['args'][0]['text']
    assert len(text) > 0 # we don't really care about the text tbh

    items = recieved[0]['args'][0]['items']
    just_created_item = [item for item in items if item['word'] == word][0]
    all_ids = [item['id'] for item in items]
    assert just_created_item['id'] == max(all_ids)
