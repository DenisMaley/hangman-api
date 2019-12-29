from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from models import UserModel


class User(Resource):
    @jwt_required
    def get(self):
        """
            This is the User API
            Call this api and get back the user - owner of the token
            ---
            tags:
              - User API
            responses:
              500:
                description: Internal Server Error
              200:
                description: A user with its details
                schema:
                  id: user
                  properties:
                    id:
                      type: string
                      description: The user id
                      default: 5e07e5e5c3fc8412c95b53c1
                    username:
                      type: string
                      description: username
                      default: Denis
        """
        user = UserModel.objects.get(pk=get_jwt_identity())

        return user.serialize(), HTTPStatus.OK
