from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

app.config.from_pyfile('conf.py')

db = SQLAlchemy(app)

limiter = Limiter(app, key_func=get_remote_address, default_limits=["1000 per day"])

from views import *

if __name__ == '__main__':
    app.run(debug = True)