from http import HTTPStatus

from flask import request
from flask_jwt_extended import (create_access_token, jwt_refresh_token_required, get_jwt_identity)
from flask_restful import Resource
from models import UserModel


class Registration(Resource):
    def post(self):
        """
            Register User
            Returns a new user model with access_token and refresh_token
            ---
            tags:
              - Auth API
            parameters:
              - name: body
                in: body
                required: true
                schema:
                  id: auth_credentials
                  required:
                    - username
                    - password
                  properties:
                    username:
                      type: string
                      description: A username for the user
                      default: "username"
                    password:
                      type: string
                      description: A username for the user
                      default: "username"
            responses:
              500:
                description: Internal Server Error
              400:
                description: Bad request
              201:
                description: The user was successfully registered
                schema:
                  id: auth_user
                  properties:
                    id:
                      type: string
                      description: The user id
                      default: 5e07e5e5c3fc8412c95b53c1
                    username:
                      type: string
                      description: username
                      default: Denis
                    access_token:
                      type: string
                      description: JWT token to access endpoints
                      default: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
                        eyJpYXQiOjE1Nzc2OTY5MjAsIm5iZiI6MTU3NzY5NjkyMCwianRpIjoiMGJjNjkzMzctYTJkMC00NTMzLTliNGQtN2Rl
                        YTZmMGZkZDEwIiwiZXhwIjoxNTc3Njk3ODIwLCJpZGVudGl0eSI6IjVlMDliZTk4MDZjZDNhMjM1MTliNTM4NCIsImZy
                        ZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.
                        OlVZGBeskZXv9kNmtZ5Vl4IgCM1-lCzSVAV8-m2FcuE
                    refresh_token:
                      type: string
                      description: JWT token to access endpoints
                      default: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
                        eyJpYXQiOjE1Nzc2OTY5MjAsIm5iZiI6MTU3NzY5NjkyMCwianRpIjoiMTAwNjZiNTAtZWFhOS00MGQ3LTk4ZTctZWE2M
                        ThiMmUyZGM3IiwiZXhwIjoxNTgwMjg4OTIwLCJpZGVudGl0eSI6IjVlMDliZTk4MDZjZDNhMjM1MTliNTM4NCIsInR5cG
                        UiOiJyZWZyZXNoIn0.
                        BSeY5AYABonwk2rvdjas-0XC20EN_Jth2Jeutz0_9d8
        """
        data = request.get_json()

        if UserModel.objects(username=data['username']):
            return {'msg': 'User already exists'}, HTTPStatus.BAD_REQUEST

        try:
            # encrypt password
            data['password'] = UserModel.generate_hash(data['password'])
            user = UserModel(**data).save()

            return user.serialize(create_token=True), HTTPStatus.CREATED
        # TODO: catch specific exceptions
        except:
            return {'msg': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR


class Login(Resource):
    def post(self):
        """
            Register User
            Returns a new user model with access_token and refresh_token
            ---
            tags:
              - Auth API
            parameters:
              - name: body
                in: body
                required: true
                schema:
                  id: auth_credentials
            responses:
              500:
                description: Internal Server Error
              400:
                description: Bad request
              200:
                description: The user was successfully logged in
                schema:
                  id: auth_user
        """
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
    # TODO: implement refresh
    def post(self):
        access_token = create_access_token(identity=get_jwt_identity())
        return {'access_token': access_token}, HTTPStatus.OK
