from flask import render_template, request, flash, redirect, url_for, session, jsonify
import requests, json, base64
from client import app, db
from models import User
from forms import RegisterForm
from passlib.hash import sha256_crypt
from functools import wraps
import os



def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You are not logged in yet, Loggin to generate your token", "danger")
            return redirect(url_for('login'))
    return wrap


#route for home
@app.route('/')
def home():
    return render_template('index.html')

#route for registering
@app.route('/register', methods = ['GET','POST'])
def register():
    #creating a form 
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():

        #retriving data from form
        fullname = form.fullname.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(form.password.data)

        #creating model with the form data
        new_user = User(fullname, email, username, password)

        #storing data into database
        db.session.add(new_user)
        db.session.commit()


        return redirect(url_for('login'))

    return render_template('register.html', form = form)


#route for login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        
        #retrive username and password directly from a html form
        username = request.form['username']
        password_candidate = request.form['password']

        login_user_data = User.query.filter_by(username = username).first() #getting user informations from db 

        #check whether a data corresponding to the respective username exist or not
        if login_user_data:

            password = login_user_data.password

            #checking whether passwords are equal
            if sha256_crypt.verify(password_candidate, password): 

                session['logged_in'] = True
                session['username'] = username

                response = requests.get('http://localhost:5000/token', auth = (username, password_candidate))
                
                tocken_data = json.loads(response.text)
                session['auth_token'] = tocken_data['token']

                flash("Your Token : {}".format(session['auth_token']), 'success')

                return redirect(url_for('img_upload'))

            else:
                error = "Invalid User Name or Password"
                return render_template('login.html', error = error)

        else:
            error = "USER NOT FOUND"
            return render_template('login.html', error = error)

    return render_template('login.html')



#route for logout
@app.route('/logout')
def logout():
    session.clear()
    flash("You are now logged out", 'success')
    return redirect(url_for('login'))


#upload image
@app.route('/img_upload', methods = ['GET', 'POST'])
@is_logged_in
def img_upload():
    
    if request.method == 'POST':
        image = request.files['image']
        image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

        directory = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)

        image_data = open(directory , 'r+b').read()

        encoded_image = base64.encodestring(image_data)

        response = requests.post('http://localhost:5000/img_upload', data = encoded_image, headers = {'auth-token': '{}'.format(session['auth_token'])})

        name = json.loads(response.text)

        return render_template('success.html', filename = name['response'])
    
    return render_template('img_upload.html')
        




    