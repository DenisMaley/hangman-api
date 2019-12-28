from http import HTTPStatus

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from models import UserModel, GameModel, WordModel


class Games(Resource):
    @jwt_required
    def post(self):
        user = UserModel.objects.get(pk=get_jwt_identity())
        word = WordModel.get_random_word()
        game = GameModel(author=user, word=word).save()

        return game.serialize(), HTTPStatus.CREATED


class Game(Resource):
    @jwt_required
    def get(self, game_id):
        game = GameModel.objects.get(pk=game_id)

        return game.serialize(), HTTPStatus.OK


class GameTurn(Resource):
    @jwt_required
    def post(self, game_id):
        data = request.get_json()
        game = GameModel.objects.get(pk=game_id)
        if game.is_pending():
            game.make_turn(data['letter'])

        return game.serialize(), HTTPStatus.CREATED
