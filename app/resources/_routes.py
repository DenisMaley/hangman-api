from .auth import Registration, Login
from .game import Games, Game, GameTurn
from .status import Status
from .user import User


def initialize_routes(api):
    api.add_resource(Status, '/status')
    api.add_resource(Registration, '/registration')
    api.add_resource(Login, '/login')
    api.add_resource(User, '/user')
    api.add_resource(Games, '/games')
    api.add_resource(Game, '/game/<string:game_id>')
    api.add_resource(GameTurn, '/game/<string:game_id>/turn')
