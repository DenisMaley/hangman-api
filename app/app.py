from flask import Flask
from flask_restful import Api
from database import initialize_db
from resources import initialize_routes

app = Flask(__name__)
api = Api(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://my_db:27017'
}

initialize_db(app)
initialize_routes(api)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
