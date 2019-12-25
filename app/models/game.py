import datetime

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

    def make_turn(self, letter):
        letter = letter.upper()
        self.named_letters.append(letter)

        if letter not in self.word.value:
            self.lives -= 1

        self.save()

    def serialize(self):
        return {
            'id': str(self.id),
            'lives': self.lives,
            'named_letters': self.named_letters,
            'disguised_word': self.get_disguised_word(),
        }
