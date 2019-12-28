from database import db
from flask_jwt_extended import create_access_token, create_refresh_token
from passlib.hash import pbkdf2_sha256 as sha256


class UserModel(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, password_hash):
        return sha256.verify(password, password_hash)

    def serialize(self, create_token=False):
        user_id = str(self.id)
        serialization = {
            'id': user_id,
            'username': self.username,
        }

        if create_token:
            serialization["access_token"] = create_access_token(identity=user_id)
            serialization["refresh_token"] = create_refresh_token(identity=user_id)

        return serialization
