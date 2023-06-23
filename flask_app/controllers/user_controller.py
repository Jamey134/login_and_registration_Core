from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
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

    query = """
    INSERT INTO users (first_name,last_name,email,password)
    VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
    """
    userData = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    userID = connectToMySQL(User.DB).query_db(query,userData)
    session['user_id']=userID
    print('new_user:', userID)
    return redirect('/testSuccess')

@app.route('/testSuccess')
def loginSuccess():
    if "user_id" not in session:
        return redirect('/') #<---- be on every routhe except the "/" route.
    user=User.GetUserByID({'id':session['user_id']})
    print(user)
    return render_template('welcomeUser.html', user = user)


@app.route('/login_user', methods = ['POST'])
def loginUser():
    login_data = {'email':request.form['email']}
    user_in_db = User.GetUserByEmail(login_data)
    if not user_in_db:
            flash("invalid email/password.")
            return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')


    user_in_db = User.GetUserByEmail(login_data)
    session['user_id'] = user_in_db.id
    print(session['user_id'])
    return redirect('/testSuccess')

@app.route('/logOut')
def logout():
    session.clear()
    return redirect('/')




    