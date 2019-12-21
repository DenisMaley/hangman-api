from http import HTTPStatus

from flask import request
from flask_restful import Resource
from models import UserModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

class Registration(Resource):
    def post(self):
        data = request.get_json()

        if UserModel.objects(username=data['username']):
            return {'message': 'User already exists'}, HTTPStatus.BAD_REQUEST

        try:
            # encrypt password
            data['password'] = UserModel.generate_hash(data['password'])
            user = UserModel(**data).save()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'id': str(user.id),
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, HTTPStatus.CREATED
        except:
            return {'message': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR


class Login(Resource):
    def post(self):
        data = request.get_json()

        if not UserModel.objects(username=data['username']):
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        current_user = UserModel.objects.get(username=data['username'])

        if UserModel.verify_hash(data['password'], current_user['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


class Logout(Resource):
    def post(self):
        return {'message': 'User logout'}


class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Token refresh'}
