from database import db


class UserModel(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    games = db.ListField(db.StringField)
