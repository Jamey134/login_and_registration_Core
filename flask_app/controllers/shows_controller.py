from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.model.user_model import User
from flask_app.model.shows_model import Shows
bcrypt = Bcrypt(app)


@app.route('/newShow')
def newShowForm():
    return render_template('newShow.html')

@app.route('/addShow', methods=['POST'])
def addShow():
    Shows.addShow(request.form)
    return redirect('/dashboard')




@app.route('/<int:show_id>/editShow')
def editShow(show_id):
    query = "SELECT * FROM shows WHERE show_id = %(id)s"
    data = {'id': show_id}
    mysql = connectToMySQL('examdb')
    show = mysql.query_db(query, data)
    return render_template("editShow.html", show = show[0])