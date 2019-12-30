from models import UserModel, WordModel, GameModel
from settings import LIVES, PLACEHOLDER
from tests import TestBase


class TestGameModel(TestBase):
    WORD = 'TESTGAME'

    @classmethod
    def setUpClass(cls):
        super(TestGameModel, cls).setUpClass()
        UserModel(username='test', password='test').save()
        WordModel(value=cls.WORD).save()

    def setUp(self):
        self.game = GameModel(
            author=UserModel.objects.first(),
            word=WordModel.objects.get(value=self.WORD)
        ).save()

    def test_get_disguised_word(self):
        self.assertEqual(' '.join([PLACEHOLDER] * len(self.WORD)), self.game.get_disguised_word())

        self.game.named_letters.append(self.WORD[0])
        # TODO Refactor it to make dependent only on self.WORD
        self.assertEqual('T _ _ T _ _ _ _', self.game.get_disguised_word())

    def test_get_word_letters_set(self):
        self.assertSetEqual(set(list(self.WORD)), self.game.get_word_letters_set())

    def test_get_named_letters_set(self):
        # TODO Refactor it to make dependent only on self.WORD
        self.game.named_letters.append('T')
        self.game.named_letters.append('T')
        self.game.named_letters.append('E')
        self.assertSetEqual({'T', 'E'}, self.game.get_named_letters_set())

    def get_guessed_letters_set(self):
        # TODO Refactor it to make dependent only on self.WORD
        self.game.named_letters.append('T')
        self.game.named_letters.append('T')
        self.game.named_letters.append('E')
        self.game.named_letters.append('W')
        self.game.named_letters.append('I')
        self.assertSetEqual({'T', 'E'}, self.game.get_named_letters_set())

    def test_is_finished(self):
        self.assertFalse(self.game.is_finished())

        self.game.lives = 0

        self.assertTrue(self.game.is_finished())

    def test_is_succeeded(self):
        self.assertFalse(self.game.is_succeeded())

        self.game.named_letters.append('W')
        self.game.named_letters.append('I')
        for letter in self.WORD:
            self.game.named_letters.append(letter)

        self.assertTrue(self.game.is_succeeded())

    def test_is_failed(self):
        self.assertFalse(self.game.is_failed())

        self.game.lives = 0

        self.assertTrue(self.game.is_failed())

    def test_is_pending(self):
        self.assertTrue(self.game.is_pending())

        self.game.lives = 0

        self.assertFalse(self.game.is_pending())

    def test_get_state(self):
        self.assertEqual('IN PROGRESS', self.game.get_state())

        self.game.lives = 0

        self.assertEqual('FAILED', self.game.get_state())

        self.game.lives += 1
        for letter in self.WORD:
            self.game.named_letters.append(letter)

        self.assertEqual('SUCCEEDED', self.game.get_state())

    def test_get_score_failed(self):
        self.game.lives = 0
        self.assertEqual(0, self.game.get_score())

        # TODO Refactor it to make dependent only on self.WORD
        self.game.named_letters.append('T')
        # 1 letter from 6 different letters: T, E, S, G, A, M.
        self.assertEqual(1 / 6 * 50, self.game.get_score())

        self.game.named_letters.append('E')
        # 2 letter from 6 different letters: T, E, S, G, A, M.
        self.assertEqual(2 / 6 * 50, self.game.get_score())

    def test_get_score_succeeded(self):
        for letter in self.WORD:
            self.game.named_letters.append(letter)

        self.assertEqual(100, self.game.get_score())

        self.game.lives -= 1

        # 1 - we have already all guessed letters
        self.assertEqual((1 + (LIVES - 1) / LIVES) * 100 / 2, self.game.get_score())

        self.game.lives -= 1

        # 1 - we have already all guessed letters
        self.assertEqual((1 + (LIVES - 2) / LIVES) * 100 / 2, self.game.get_score())

    def test_make_turn(self):
        self.assertEqual(0, self.game.score)
        self.assertIsNone(self.game.finish_timestamp)

        self.game.make_turn('W')

        self.assertIn('W', self.game.named_letters)
        self.assertEqual(LIVES - 1, self.game.lives)

        self.game.make_turn('I')

        self.assertIn('W', self.game.named_letters)
        self.assertEqual(LIVES - 2, self.game.lives)

        for letter in self.WORD:
            self.game.make_turn(letter)
            self.assertIn(letter, self.game.named_letters)
            self.assertEqual(LIVES - 2, self.game.lives)

        self.assertEqual((1 + (LIVES - 2) / LIVES) * 100 / 2, self.game.score)
        self.assertIsNotNone(self.game.finish_timestamp)

    def test_serialize(self):
        for letter in self.WORD:
            self.game.make_turn(letter)

        serialization = self.game.serialize()

        self.assertIsNotNone(serialization['id'])
        self.assertEqual(LIVES, serialization['lives'])
        self.assertListEqual(list(self.WORD), serialization['named_letters'])
        self.assertEqual(' '.join(list(self.WORD)), serialization['disguised_word'])
        self.assertEqual('SUCCEEDED', serialization['state'])
        self.assertIsNotNone(serialization['started_at'])
        self.assertEqual(100, serialization['score'])
        self.assertIsNotNone(serialization['finished_at'])
