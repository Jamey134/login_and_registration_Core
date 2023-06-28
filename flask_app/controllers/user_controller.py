from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User
from flask_app.models.tree_model import Tree
bcrypt = Bcrypt(app)

#App Routing means mapping the URLs to a specific function that will handle the logic for that URL.

#THIS IS THE HOMEPAGE
@app.route('/')
def home():
    return render_template('home.html')

#THIS FUNCTION CREATES THE USER
@app.route('/user/create', methods=['POST']) #<--- METHOD POST ALWAYS GO WITH THE REDIRECT FUNCTION.
#THIS IS VALIDATING THE USER
def validateUser():
#IF USER IS INVALID, THEN USER WILL BE SENT TO HOMEPAGE
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
#THIS IS WHERE I CREATE A DIC FOR THE FUNCTION TO GRAB DATA FROM THE MODEL CLASS
    userData = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
# CREATE A VARIABLE TO CALL CLASS FUNCTION WITH DIC ABOVE.
    user = User.create(userData)
    session['id'] = user
    print('new_user:', user)
    return redirect('/dashboard')


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

    session['id'] = user_in_db.id
    print(session['id'])
    return redirect('/dashboard') #<--- REROUTE TO DASHBOARD.HTML


@app.route('/logout') #<--- USE ROUTE FOR ALL APPS
def logout():
    session.clear()
    return redirect('/')

@app.route('/myTrees')
def manageMyTrees():
        if "id" not in session:
            flash("PLEASE LOGIN!")
        return redirect('/')
        one_user = User.get_user_with_trees({"user_id":session['user_id']})
        return render_template('MyTree.html', one_user=one_user)

#==============EXTRA ROUTES FOR FUTURE EXAM===========
@app.route('/user/edit/')
def editUser():
    if "user_id" not in session:
        return redirect('/') 
    editUser = User.GetUserByID({'id':session['user_id']}) 
    print('HERE', editUser)
    return render_template('editUser.html', editUser = editUser)

@app.route('/user/update',methods=['POST']) #METHODS POST IS NEEDED
def updateUser():
    if not User.validateUpdate(request.form):
        return redirect('/user/edit/')
    userData = {
        'user_id': session['user_id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name']
    }
    User.edit(userData) #<--- CALLING THE FUNCTION FROM CLASS AND ENTERING DATA IN PARAMETER
    return redirect('/testSuccess')#<--- REROUTE TO DASHBOARD.HTML

@app.route('/user/delete/<int:user_id>') #<--- Add ID in parameter to target a specific user
def delete(user_id): #<--- ADD ID INTO PARAMETER
    if "user_id" not in session:
        return redirect('/') 
    User.delete(user_id) #<--- Calling the function targeting user_id's
    return redirect('/') #<--- TAKES US BACK TO HOMEPAGE

