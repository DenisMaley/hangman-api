import unittest

from migrations import set_up_db
from mongoengine import connect, disconnect


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')
        set_up_db()

    @classmethod
    def tearDownClass(cls):
        disconnect()
