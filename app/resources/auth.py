from http import HTTPStatus

from flask import request
from flask_jwt_extended import (create_access_token, jwt_refresh_token_required, get_jwt_identity)
from flask_restful import Resource
from models import UserModel


class Registration(Resource):
    def post(self):
        data = request.get_json()

        if UserModel.objects(username=data['username']):
            return {'msg': 'User already exists'}, HTTPStatus.BAD_REQUEST

        try:
            # encrypt password
            data['password'] = UserModel.generate_hash(data['password'])
            user = UserModel(**data).save()

            return user.serialize(create_token=True), HTTPStatus.CREATED
        except:
            return {'msg': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR


class Login(Resource):
    def post(self):
        data = request.get_json()

        if not UserModel.objects(username=data['username']):
            return {'msg': 'User {} doesn\'t exist'.format(data['username'])}, HTTPStatus.BAD_REQUEST

        user = UserModel.objects.get(username=data['username'])

        if UserModel.verify_hash(data['password'], user.password):
            return user.serialize(create_token=True), HTTPStatus.OK
        else:
            return {'msg': 'Wrong credentials'}, HTTPStatus.UNAUTHORIZED


class Logout(Resource):
    # TODO: implement logout: get rid of tokens
    def post(self):
        pass


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        access_token = create_access_token(identity=get_jwt_identity())
        return {'access_token': access_token}, HTTPStatus.OK
