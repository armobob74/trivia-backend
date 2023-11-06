from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    games = db.relationship('Game', backref='manager', lazy=True)

class Game(db.Model):
    id = db.Column(db.String(4), primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=False)

class DemoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String)
