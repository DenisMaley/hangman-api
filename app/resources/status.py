from http import HTTPStatus

from flask_restful import Resource


class Status(Resource):
    def get(self):
        return {"status": "OK"}, HTTPStatus.OK
