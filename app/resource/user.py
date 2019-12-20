from http import HTTPStatus

import bcrypt
from flask import request
from flask_restful import Resource

from project_db import db


class User(Resource):
    def get(self, username):
        user = db.users.find_one({"username": username})
        result = {
            "user": {
                "username": user["username"],
                "games": user["games"]
            }
        }
        return result, HTTPStatus.OK


class UserList(Resource):
    def post(self):
        # Get posted data from request
        data = request.get_json()

        # get data
        username = data["username"]
        password = data["password"]

        # encrypt password
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # Insert record
        db.users.insert({
            "username": username,
            "password": hashed_pw,
            "games": []
        })

        result = {"msg": "User was registered"}
        return result, HTTPStatus.CREATED
