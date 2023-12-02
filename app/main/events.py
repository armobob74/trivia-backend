import pdb
from flask import session
from flask_socketio import emit, join_room, leave_room, close_room
from ..models import Game, db, Manager, Player
from .. import socketio


@socketio.on('manage-game', namespace='/')
def manageGame(message):
    """
    Sent whenever manager opens console
    Subscribes manager to the manage-{game_id} room
    """
    game_id = message['game-id']
    room = f"manage-{game_id}"
    join_room(room)
    emit('manage-game-response',{'text':f'Managing game {game_id}'}, room=room)

@socketio.on('join-game', namespace='/')
def joinGame(message):
    """
    Sent by players when they join a game.
    Server relays this information to management console.
    Server does not need to update database, as database is informed of player during create-player event.
    """
    game_id = message['game-id']
    username = message['username']
    
    join_room(game_id)
    emit('join-game', {'text': f'joined game {game_id}'})
    emit('join-game',{'username':username}, room=f'manage-{game_id}')

@socketio.on('end-game', namespace='/')
def endGame(message):
    """
    Sent after game is completed
    """
    room = message['game-id']
    emit('end-game', {'text': f'Closing room {room}'}, room=room)
    close_room(room)

@socketio.on('create-manager', namespace='/')
def createManager(message):
    manager = Manager()
    db.session.add(manager)
    db.session.commit()
    game_id = message['game-id']
    join_room(f'manage-{game_id}')
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
