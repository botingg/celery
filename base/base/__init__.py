from flask import Flask
from flask_restx import Api

from apis.acount.api import api as account_ns
import config
from db import Database

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config.DevelopmentConfig)

api = Api(app, version='0.0.1',
          title='Flask-RESTX and Swagger test', doc='/api/doc')

api.add_namespace(account_ns)

Database.initial()