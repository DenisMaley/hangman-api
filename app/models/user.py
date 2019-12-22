from database import db
from passlib.hash import pbkdf2_sha256 as sha256

from .game import GameModel


class UserModel(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    games = db.EmbeddedDocumentListField(GameModel)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, password_hash):
        return sha256.verify(password, password_hash)
