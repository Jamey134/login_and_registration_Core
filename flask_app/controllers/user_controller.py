from flask_app import app
from flask import render_template, redirect, request
from flask_bcrypt import Bcrypt

from flask_app.model.user_model import User
bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return redirect('/user')

@app.route('/user')
def home():
    return render_template('home.html')