import unittest

from models import WordModel
from settings import INITIAL_WORDS
from tests import TestBase


class TestWordModel(TestBase):

    def test_get_random_word(self):
        word = WordModel.get_random_word()

        self.assertIn(word.value, [x.upper() for x in INITIAL_WORDS])


if __name__ == '__main__':
    unittest.main()
