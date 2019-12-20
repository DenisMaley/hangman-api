from flask import Flask
from flask_restful import Api

from resource import *

app = Flask(__name__)
api = Api(app)

# Since we have only few endpoints, let's keep the routing here for now
api.add_resource(Status, '/status')
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/users/<string:username>', endpoint='user')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
