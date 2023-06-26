from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.model.user_model import User
from flask_app.model.shows_model import Shows
bcrypt = Bcrypt(app)


#DASHBOARD
@app.route('/dashboard') 
def loginSuccess():
    if "user_id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')  #<--- be on every route except the "/" route.
    user = User.GetUserByID({'id': session['user_id']})
    
    print(user)
    return render_template('dashboard.html', user=user)


# DIRECTS USER TO NEWSHOW.HTML TO ADD NEW SHOW
@app.route('/newShow')
def newShowForm():
    if "user_id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')
    return render_template('newShow.html')

#CREATE A NEW SHOW
@app.route('/addShow', methods=['POST'])
def addShow():
    if "user_id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')
    Shows.addShow(request.form)
    return redirect('/dashboard')

#EDIT A SHOW
@app.route('/editShow/<int:show_id')
def editShow(show_id):
    query = "SELECT * FROM shows WHERE show_id = %(id)s"
    data = {'id': show_id}
    mysql = connectToMySQL('examdb')
    show = mysql.query_db(query, data)
    return render_template("editShow.html", show = show[0])