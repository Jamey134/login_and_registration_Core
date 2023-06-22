from flask_app import app
from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt

from flask_app.model.user_model import User
bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user/create', methods = ['POST'])
def validateUser():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    userData = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    session['user_id']=User.save(userData)
    return redirect('/testSuccess')

@app.route('/testSuccess')
def loginSuccess():
    user=User.GetUserByID({'id':session['user_id']})
    return render_template('welcomeUser.html', user = user)