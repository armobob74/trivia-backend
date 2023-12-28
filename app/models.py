from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    games = db.relationship('Game', backref='manager', lazy=True)

class Game(db.Model):
    id = db.Column(db.String(4), primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=False)
    players = db.relationship('Player', backref='game', lazy=True)  # One-to-many relationship with Player
    question_index = db.Column(db.Integer, default=0)
    questions = db.Column(db.String)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    game_id = db.Column(db.String(4), db.ForeignKey('game.id'), nullable=False)  # Foreign key to Game
    score = db.Column(db.Integer, default=0)
    answer = db.Column(db.String, default='')
    answer_is_correct = db.Column(db.Boolean, default=False)
