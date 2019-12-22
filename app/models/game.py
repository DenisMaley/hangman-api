import datetime

from bson.objectid import ObjectId
from database import db


class GameModel(db.EmbeddedDocument):
    _id = db.ObjectIdField(required=True, default=ObjectId, unique=True, primary_key=True)
    start_timestamp = db.DateTimeField(default=datetime.datetime.now)
    level = db.IntField(default=0)
