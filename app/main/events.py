import pdb
import json
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
    game = Game.query.get(game_id)
    players = game.players
    player_info = [{'username':p.username, 'score':p.score,'answer':p.answer, 'answer_is_correct':p.answer_is_correct} for p in players]
    print('manager connected')
    response = {
            'text':f'Managing game {game_id}',
            'players':player_info,
            'question_idx':game.question_index
            }
    print(response)
    emit('manage-game-response',response, room=room)

@socketio.on('join-game', namespace='/')
def joinGame(message):
    """
    Sent by players when they join a game.
    Server relays this information to management console.
    Server does not need to update database, as database is informed of player during create-player event.
    """
    game_id = message['game-id']
    username = message['username']

    game = Game.query.get(game_id)
    questions = json.loads(game.questions)
    question = questions[game.question_index]
    
    join_room(game_id)
    emit('join-game', {'text': f'joined game {game_id}', 'question':question}, room=game_id)
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
            Game(id=message['game-id'], manager_id=message['manager-id'], questions=message['questions'])
    )
    db.session.commit()
    emit('create-game-response')

@socketio.on('create-player',namespace='/')
def createPlayer(message):
    username = message['username']
    game_id = message['game_id']
    game = Game.query.get(game_id)
    if username in [p.username for p in game.players]:
        emit('create-player-response',{
            'ok':False,
            'text': f'Player "{username}" already exists in this game'
            })
    else:
        player = Player(username = username, game_id = game_id)
        db.session.add(player)
        db.session.commit()
        emit('create-player-response', {
            'ok':True,
            'text':f'player created with username {username} for game {game_id}',
            'player-id':player.id
            })

@socketio.on('next-question', namespace='/')
def nextQuestion(message):
    game_id = message['game-id']
    question = message['question']
    game = Game.query.get(game_id)
    game.question_index += 1;
    for player in game.players:
        # score is set by front end because front end has accurate info about checkbox condition
        # answer and answer_is_correct are simultaniously reset on front end and back end on next-question

        player.answer = ''
        player.answer_is_correct = False
    db.session.commit()
    emit('next-question',{'question':question}, room=game_id)

@socketio.on('change-score', namespace='/')
def changeScore(message):
    """
    message fields:
        game_id
        username
        delta
    """
    game_id = message['game-id']
    username = message['username']
    delta = message['delta']
    game = Game.query.get(game_id)
    player = [p for p in game.players if p.username == username][0]
    player.score += delta;
    print(username, 'score: ', player.score) 
    db.session.commit()
    pass
    

@socketio.on('submit-answer', namespace='/')
def submitAnswer(message):
    """
    Recieve submission from player and forward the information to manager and database
    Manager decides correctness of answer

    message fields:
        username
        game_id
        answer
    """
    game_id = message['game-id']
    username = message['username']
    answer = message['answer']
    game = Game.query.get(game_id)

    questions = json.loads(game.questions)
    question = questions[game.question_index]
    correct_answer = question[question['correct']]

    player_index = [p.username for p in game.players].index(username)
    player = game.players[player_index]
    player.answer = answer

    # determine the initial correctnes of answer.
    # manager has authority to change this by unchecking box in UI
    # This is necessary for manager console loading

    if answer.lower() == correct_answer.lower():
        player.answer_is_correct = True
    else:
        player.answer_is_correct = False
    db.session.commit()
    emit('submit-answer',message,room=f'manage-{game_id}')
    pass
    
