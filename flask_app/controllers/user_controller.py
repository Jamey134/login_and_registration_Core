from flask_app import app
from flask import render_template, redirect, request
from flask_bcrypt import Bcrypt

from flask_app.model.user_model import User
bcrypt = Bcrypt(app)


@app.route('/')
@app.route('/user', methods = ['POST'])
def home():
    User.save
    return render_template('home.html')

