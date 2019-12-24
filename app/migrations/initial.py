from models import WordModel
from settings import INITIAL_WORDS


def set_up_db():
    word_collection = []
    for word in INITIAL_WORDS:
        word_collection.append(WordModel(value=word))
    WordModel.objects.insert(word_collection, load_bulk=True)
