from http import HTTPStatus

from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity)
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
            user_id = str(user.id)

            access_token = create_access_token(identity=user_id)
            refresh_token = create_refresh_token(identity=user_id)
            return {
                       'id': user_id,
                       'access_token': access_token,
                       'refresh_token': refresh_token,
                   }, HTTPStatus.CREATED
        except:
            return {'msg': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR


class Login(Resource):
    def post(self):
        data = request.get_json()

        if not UserModel.objects(username=data['username']):
            return {'msg': 'User {} doesn\'t exist'.format(data['username'])}, HTTPStatus.BAD_REQUEST

        current_user = UserModel.objects.get(username=data['username'])

        if UserModel.verify_hash(data['password'], current_user['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                       'msg': 'Logged in as {}'.format(current_user['username']),
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, HTTPStatus.OK
        else:
            return {'msg': 'Wrong credentials'}, HTTPStatus.UNAUTHORIZED


class Logout(Resource):
    def post(self):
        return {'msg': 'User logout'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}
