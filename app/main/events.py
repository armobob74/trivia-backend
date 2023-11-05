from flask import session
from flask_socketio import emit, join_room, leave_room, close_room
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
