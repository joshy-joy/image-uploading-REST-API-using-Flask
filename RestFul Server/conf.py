import os


#database configuration
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'REST_db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = True


#Encryption and Authorization
SECRET_KEY = 'ImAgE@UpLoAd@ApP$26-9-2019'

#image save location
IMAGE_UPLOADS = os.path.join(basedir, 'uploads')