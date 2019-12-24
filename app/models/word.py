from random import randint

from database import db


class WordModel(db.Document):
    word = db.StringField(required=True)

    @staticmethod
    def get_random_word():
        random_int = randint(0, WordModel.objects.count() - 1)
        return WordModel.objects[random_int]
