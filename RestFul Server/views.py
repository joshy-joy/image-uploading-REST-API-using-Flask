from flask import render_template, request, Response, jsonify
import jsonpickle
from run import app
import jwt, base64, uuid, os
import datetime
from models import imageData, User
from run import db, limiter
from functools import wraps


#decorator to varify token
def varify_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        data = jwt.decode(token, app.config['SECRET_KEY'])
        current_user = User.query.filter_by(username = data['username']).first()
        if current_user:
            return f(*args, **kwargs)
        else:
            response = {'response' : 'invalid token'}
            response_pickled = jsonpickle.encode(response)
            return Response(response = response_pickled, status=200, mimetype="application/json")
    return decorator


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/token', methods = ['GET'])
def token():
    auth = request.authorization
    jwt_token = jwt.encode({"username": auth.username, "exp":datetime.datetime.utcnow()+ datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
    print(jwt_token)
    response = {'token' : '{}'.format(jwt_token)}
    response_pickled = jsonpickle.encode(response)

    new_user = User(auth.username)

    db.session.add(new_user)
    db.session.commit()


    return Response(response = response_pickled, status=200, mimetype="application/json")



@app.route('/img_upload', methods = ['POST'])
#@varify_token
@limiter.limit("5/minute")
def upload():
    
    data = request.data
    
    image_decode = base64.decodestring(data)
    filename = str(uuid.uuid4())
    directory = os.path.join(app.config["IMAGE_UPLOADS"],filename)
    image_result = open(directory, 'w+b')

    image_result.write(image_decode)

    new_data = imageData(filename, directory)

    db.session.add(new_data)
    db.session.commit()

    response = {'response' : '{}'.format(filename)}
    response_pickled = jsonpickle.encode(response)

    return Response(response = response_pickled, status=200, mimetype="application/json")