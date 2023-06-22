from flask_app import app
from flask import render_template, redirect, request
from flask_bcrypt import Bcrypt

from flask_app.model.user_model import User
bcrypt = Bcrypt(app)


@app.route('/')
@app.route('/user')
def home():
    User.save
    return render_template('home.html')

@app.route('/user/validate', methods = ['POST'])
def validateUser():
    if not User.validate_user(request.form):
        return redirect('/')
    return redirect('/testSuccess')

@app.route('/testSuccess')
def loginSuccess():
    return render_template('welcomeUser.html')