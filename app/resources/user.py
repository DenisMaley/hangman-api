from http import HTTPStatus

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models import UserModel


class User(Resource):
    @jwt_required
    def get(self, username):
        user = UserModel.objects(username=username).to_json()

        return Response(user, mimetype="application/json", status=HTTPStatus.OK)
