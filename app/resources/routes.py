from .status import Status
from .user import User, UserList


def initialize_routes(api):
    api.add_resource(Status, '/status')
    api.add_resource(UserList, '/users', endpoint='users')
    api.add_resource(User, '/users/<string:username>', endpoint='user')
