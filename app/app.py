from database import initialize_db
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from migrations import set_up_db
from resources import initialize_routes

app = Flask(__name__)
cors = CORS(app)
api = Api(app, '/api')

app.config['JWT_SECRET_KEY'] = 'app-jwt-secret-string'
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://my_db:27017'
}

jwt = JWTManager(app)
initialize_db(app)
set_up_db()
initialize_routes(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
