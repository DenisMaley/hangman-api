import datetime

from database import db
from settings import LIVES, PLACEHOLDER

from .user import UserModel
from .word import WordModel


class GameModel(db.Document):
    author = db.ReferenceField(UserModel, required=True)
    word = db.ReferenceField(WordModel, required=True)
    lives = db.IntField(default=LIVES)
    start_timestamp = db.DateTimeField(default=datetime.datetime.now)
