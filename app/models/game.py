import datetime

from bson import json_util
from database import db
from settings import LIVES, PLACEHOLDER

from .user import UserModel
from .word import WordModel


class GameModel(db.Document):
    author = db.ReferenceField(UserModel, required=True)
    word = db.ReferenceField(WordModel, required=True)
    named_letters = db.ListField()
    lives = db.IntField(default=LIVES)
    start_timestamp = db.DateTimeField(default=datetime.datetime.now)

    def get_disguised_word(self):
        symbols = []

        for letter in self.word.value:
            if letter in self.named_letters:
                symbols.append(letter)
            else:
                symbols.append(PLACEHOLDER)

        return ' '.join(symbols)

    def to_json(self, *args, **kwargs):
        use_db_field = kwargs.pop("use_db_field", False)

        default_fields = ['lives', 'named_letters']
        fields = kwargs.pop("fields", default_fields)

        bson_game = self.to_mongo(use_db_field, fields)
        bson_game['disguised_word'] = self.get_disguised_word()

        return json_util.dumps(bson_game, *args, **kwargs)
