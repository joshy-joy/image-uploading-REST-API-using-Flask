from run import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200))

    def __init__(self,username):

        self.username = username



class imageData(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    image_name = db.Column(db.String(200))
    image_path = db.Column(db.String(500))

    def __init__(self,image_name, image_path):

        self.image_name = image_name
        self.image_path = image_path

