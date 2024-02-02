import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

liked_games_table = db.Table(
    'games_likes',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),

    db.Column(
        'game_id', db.Integer,
        db.ForeignKey('games.id'),
        primary_key=True
    )
)

liked_runs_table = db.Table(
    'runs_likes',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),

    db.Column(
        'run_id', db.Integer,
        db.ForeignKey('runs.id'),
        primary_key=True
    )
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    runs = db.relationship('Run', secondary=liked_runs_table, backref='user', cascade='all,delete')
    games = db.relationship('Game', secondary=liked_games_table, backref='user', cascade='all,delete')

    def __init__(self, name:str, profile_id:int):
        self.name=name
        self.profile_id=profile_id
    
    def serialize(self):
        return{
            'id':self.id,
            'name':self.name,
            'profile_id':self.profile_id
        }


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    address = db.Column(db.String(128), nullable=False)

    def __init__(self, email:str, address:str):
        self.email=email
        self.address=address

    def serialize(self):
        return{
            'id':self.id,
            'email':self.email,
            'address':self.address
        }

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)

    liking_users = db.relationship(
        'User', secondary=liked_games_table,
        lazy='subquery',
        backref=db.backref('liked_games',lazy=True)
    )

    def __init__(self, name:str):
        self.name=name
    
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name
        }

class Run(db.Model):
    __tablename__ = 'runs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    time = db.Column(db.Interval, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    liking_users = db.relationship(
        'User', secondary=liked_runs_table,
        lazy='subquery',
        backref=db.backref('liked_runs',lazy=True)
    )

    def __init__(self, time:db.Interval, game_id:int, user_id:int):
        self.time=time
        self.game_id=game_id
        self.user_id=user_id
    
    def serialize(self):
        return{
            'id': self.id,
            'date': self.date.isoformat(),
            'time': str(self.time),
            'game_id': self.game_id,
            'user_id': self.user_id
        }



