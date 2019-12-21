from .status import Status
from .user import User
from .auth import Registration, Login


def initialize_routes(api):
    api.add_resource(Status, '/status')
    api.add_resource(Registration, '/registration')
    api.add_resource(Login, '/login')
    api.add_resource(User, '/users/<string:username>')
