from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#configuring the app
app.config.from_pyfile('config.py') #from config.py


#initialize database
db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run(debug=True, port=5001)