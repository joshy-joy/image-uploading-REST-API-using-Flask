from client import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(200))
    email = db.Column(db.String(100), unique = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(200))

    def __init__(self, fullname, email, username, password):

        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password


