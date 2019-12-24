from http import HTTPStatus

from flask import Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from models import UserModel, GameModel


class Games(Resource):
    @jwt_required
    def post(self):
        user = UserModel.objects.get(pk=get_jwt_identity())
        game = GameModel(author=user).save()

        return Response(game.to_json(), mimetype="application/json", status=HTTPStatus.OK)


class Game(Resource):
    @jwt_required
    def get(self, game_id):
        game = GameModel.objects.get(pk=game_id)

        return Response(game.to_json(), mimetype="application/json", status=HTTPStatus.OK)
