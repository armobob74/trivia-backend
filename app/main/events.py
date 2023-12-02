import pdb
from flask import session
from flask_socketio import emit, join_room, leave_room, close_room
from ..models import Game, db, Manager, Player
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

@socketio.on('create-manager', namespace='/')
def createManager():
    manager = Manager()
    db.session.add(manager)
    db.session.commit()
    emit('create-manager-response', {'manager-id':manager.id})

@socketio.on('create-game', namespace='/')
def createGame(message):
    db.session.add(
            Game(id=message['game-id'], manager_id=message['manager-id'])
    )
    db.session.commit()
    emit('create-game-response')

@socketio.on('create-player',namespace='/')
def createPlayer(message):
    username = message['username']
    game_id = message['game_id']
    db.session.add(
            Player(username = username, game_id = game_id)
            )
    db.session.commit()
    emit('create-player-response', {'text':f'player created with username {username} for game {game_id}'})
