from http import HTTPStatus

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from models import GameModel, UserModel


class Games(Resource):
    @jwt_required
    def post(self):
        user = UserModel.objects.get(pk=get_jwt_identity())
        data = request.get_json()
        game = user.games.create(**data)
        user.save()

        return Response(game.to_json(), mimetype="application/json", status=HTTPStatus.OK)


class Game(Resource):
    @jwt_required
    def get(self, game_id):
        user = UserModel.objects.get(pk=get_jwt_identity())
        game = user.games.get(_id=game_id)

        return Response(game.to_json(), mimetype="application/json", status=HTTPStatus.OK)
