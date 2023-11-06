import pdb
from flask import session
from flask_socketio import emit, join_room, leave_room, close_room
from ..models import db, DemoModel
from .. import socketio

@socketio.on('join-game', namespace='/')
def joinGame(message):
    """
    Sent by players when they join a game.
    Server relays this information to management console.
    """
    game_id = message['game-id']
    join_room(game_id)
    emit('join-game', {'text': f'joined game {game_id}'})

@socketio.on('end-game', namespace='/')
def endGame(message):
    """
    Sent after game is completed
    """
    room = message['game-id']
    emit('end-game', {'text': f'Closing room {room}'}, room=room)
    close_room(room)

@socketio.on('create-item-demo', namespace='/')
def endGame(message):
    """
    create an object in the database for test purposes
    """
    demo = DemoModel(word = message['demo-model']['word'])
    db.session.add(demo)
    db.session.commit()
    all_models = DemoModel.query.all()
    # now make items json-serializable
    items = []
    for model in all_models:
        d = model.__dict__
        keys = [key for key in d.keys() if not key.startswith('_')]
        item = {key:d[key] for key in keys}
        items.append(item)
    emit('create-item-demo', {'text': f'item added to db','items':items})
