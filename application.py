#from flaskr import create_app
#from flaskr.vistas.vistas import VistaPing, VistaBlack, VistaIsBlack, VistaToken
#from flaskr.modelos.modelos import db, BlackMail
from flask_restful import Api
from flask_jwt_extended import JWTManager


import datetime
from flask import Flask
import os

def create_app(config_name):
    app=Flask(__name__)
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'devops2023'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

    if 'RDS_HOSTNAME' in os.environ:
        NAME=os.environ['RDS_DB_NAME']
        USER=os.environ['RDS_USERNAME']
        PASSWORD=os.environ['RDS_PASSWORD']
        HOST=os.environ['RDS_HOSTNAME']
        PORT=os.environ['RDS_PORT']
        app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/blacklist'     
    return app


application=create_app('default')
app_context=application.app_context()
app_context.push()


from datetime import datetime
import uuid
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, verify_jwt_in_request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
#from flaskr.modelos.modelos import db, BlackMail, BlackMailSchema
from flask_jwt_extended.exceptions import NoAuthorizationError
from functools import wraps
from jwt import InvalidSignatureError, ExpiredSignatureError, InvalidTokenError

#blackMail_schema = BlackMailSchema()

def authorization_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()     
                user_jwt=str(int(get_jwt_identity()))
                if user_jwt=='1':
                    return fn(*args, **kwargs)
                else:
                    return "Ataque Detectado"
            except InvalidSignatureError:
                return "Signature verification failed"
            except NoAuthorizationError:
                return "Missing JWT"
            except Exception as inst:
                print(type(inst))    # the exception instance
                return "Usuario Desautorizado"
        return decorator
    return wrapper


class VistaPing(Resource):
    def get(self):
        print("pong")
        return {"Mensaje":"Pong"}, 200

class VistaEnv(Resource):
    def get(self):
        print("Environment")
        return {
            "RDS_DB_NAME":os.environ['RDS_DB_NAME'],
            "RDS_USERNAME":os.environ['RDS_USERNAME'],
            "RDS_PASSWORD":os.environ['RDS_PASSWORD'],
            "RDS_HOSTNAME":os.environ['RDS_HOSTNAME'],
            "RDS_PORT":os.environ['RDS_PORT'],
            "URL_DATABASE":application.config['SQLALCHEMY_DATABASE_URI'],
        }, 200

api = Api(application)
#api.add_resource(VistaBlack, '/blacklists/')
#api.add_resource(VistaIsBlack, '/blacklists/<string:email>')
api.add_resource(VistaPing, '/blacklists/ping')
api.add_resource(VistaEnv, '/blacklists/env')

jwt = JWTManager(application)

if __name__ == "__main__":
    application.run(port = 5000, debug = True)
