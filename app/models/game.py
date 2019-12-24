import datetime

from database import db

from .user import UserModel


class GameModel(db.Document):
    author = db.ReferenceField(UserModel, required=True)
    start_timestamp = db.DateTimeField(default=datetime.datetime.now)
