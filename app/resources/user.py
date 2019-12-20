from http import HTTPStatus

import bcrypt
from flask import Response, request
from flask_restful import Resource
from models import UserModel


class User(Resource):
    def get(self, username):
        user = UserModel.objects.get(username=username).to_json()
        return Response(user, mimetype="application/json", status=HTTPStatus.OK)


class UserList(Resource):
    def post(self):
        # Get posted data from request
        data = request.get_json()

        # encrypt password
        data["password"] = bcrypt.hashpw(data["password"].encode('utf8'), bcrypt.gensalt())

        user = UserModel(**data).save()

        result = {"msg": "User was registered"}
        return Response(result, mimetype="application/json", status=HTTPStatus.CREATED)
