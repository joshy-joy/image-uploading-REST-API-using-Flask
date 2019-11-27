import os


#database configuration
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = True

#image save location
IMAGE_UPLOADS = os.path.join(basedir, 'uploads')

#Encryption and Authorization
SECRET_KEY = 'ImAgE@UpLoAd@ApP$26-9-2019'