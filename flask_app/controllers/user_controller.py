from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.model.user_model import User
from flask_app.model.shows_model import Shows
bcrypt = Bcrypt(app)

#THIS IS THE HOMEPAGE
@app.route('/')
def home():
    return render_template('home.html')

#THIS FUNCTION CREATES THE USER
@app.route('/user/create', methods=['POST'])
#THIS IS VALIDATING THE USER
def validateUser():
#IF USER IS INVALID, THEN USER WILL BE SENT TO HOMEPAGE
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    userData = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }

    user = User.create(userData)
    session['user_id'] = user
    print('new_user:', user)
    return redirect('/testSuccess')


@app.route('/testSuccess')
def loginSuccess():
    if "user_id" not in session:
        return redirect('/')  # <---- be on every route except the "/" route.
    user = User.GetUserByID({'id': session['user_id']})
    print(user)
    return render_template('dashboard.html', user=user)


@app.route('/login_user', methods=['POST'])
def loginUser():
    login_data = {'email': request.form['email']}
    user_in_db = User.GetUserByEmail(login_data)
    if not user_in_db:
        flash("invalid email/password.")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')

    user_in_db = User.GetUserByEmail(login_data)
    session['user_id'] = user_in_db.user_id
    print(session['user_id'])
    return redirect('/testSuccess')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/user/edit/')
def editUser():
    editUser = User.GetUserByID({'id':session['user_id']})
    print('HERE', editUser)
    return render_template('editUser.html', editUser = editUser[0])

@app.route('/user/update',methods=['POST'])
def updateUser():
    if not User.validateUpdate(request.form):
        return redirect('/user/edit/')
    userData = {
        'user_id': session['user_id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name']
    }
    User.edit(userData)
    return redirect('/testSuccess')

