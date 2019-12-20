from http import HTTPStatus

from flask_restful import Resource


class Status(Resource):
    def get(self):
        result = {"status": "OK"}
        return result, HTTPStatus.OK
