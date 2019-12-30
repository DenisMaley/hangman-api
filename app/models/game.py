import datetime

from database import db
from settings import LIVES, PLACEHOLDER

from .user import UserModel
from .word import WordModel


class GameModel(db.Document):
    author = db.ReferenceField(UserModel, required=True)
    word = db.ReferenceField(WordModel, required=True)
    named_letters = db.ListField()
    lives = db.IntField(min_value=0, max_value=LIVES, default=LIVES)
    start_timestamp = db.DateTimeField(default=datetime.datetime.utcnow)
    finish_timestamp = db.DateTimeField()
    score = db.IntField(min_value=0, max_value=100, default=0)

    def get_disguised_word(self):
        symbols = []

        for letter in self.word.value:
            if letter in self.named_letters:
                symbols.append(letter)
            else:
                symbols.append(PLACEHOLDER)

        return ' '.join(symbols)

    def get_word_letters_set(self):
        return set(list(self.word.value))

    def get_named_letters_set(self):
        return set(self.named_letters)

    def get_guessed_letters_set(self):
        word_letters = self.get_word_letters_set()
        named_letters = self.get_named_letters_set()
        return word_letters.intersection(named_letters)

    def is_finished(self):
        return self.is_succeeded() or self.is_failed()

    def is_succeeded(self):
        return self.lives > 0 and self.get_word_letters_set() <= self.get_named_letters_set()

    def is_failed(self):
        return self.lives == 0

    def is_pending(self):
        return not self.is_finished()

    def get_state(self):
        if self.is_failed():
            return 'FAILED'
        elif self.is_succeeded():
            return 'SUCCEEDED'
        elif self.is_pending():
            return 'IN PROGRESS'

    def get_score(self):
        score = 0
        if self.is_finished():
            score_parts = [
                self.lives / LIVES,
                len(self.get_guessed_letters_set()) / len(self.get_word_letters_set())
            ]
            score = sum(score_parts) / len(score_parts) * 100
        return score

    def make_turn(self, letter):
        letter = letter.upper()
        self.named_letters.append(letter)

        if letter not in self.word.value:
            self.lives -= 1

        if self.is_finished() and not self.finish_timestamp:
            self.finish_timestamp = datetime.datetime.utcnow()
            self.score = self.get_score()

        self.save()

    def serialize(self):
        serialization = {
            'id': str(self.id),
            'lives': self.lives,
            'named_letters': self.named_letters,
            'disguised_word': self.get_disguised_word(),
            'state': self.get_state(),
            'started_at': str(self.start_timestamp),
            'score': self.get_score(),
        }

        if self.finish_timestamp:
            serialization['finished_at'] = str(self.finish_timestamp)

        return serialization
