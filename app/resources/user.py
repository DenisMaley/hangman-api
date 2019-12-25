from http import HTTPStatus

from flask import Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from models import UserModel


class User(Resource):
    @jwt_required
    def get(self):
        user = UserModel.objects.get(pk=get_jwt_identity())

        return user.serialize(), HTTPStatus.OK
