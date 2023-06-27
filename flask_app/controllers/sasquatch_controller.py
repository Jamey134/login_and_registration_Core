from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.model.user_model import User
from flask_app.model.sasquatch_model import Sasquatch
bcrypt = Bcrypt(app)


#DASHBOARD
@app.route('/dashboard') 
def loginSuccess():
    if "id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')  #<--- be on every route except the "/" route.
    user = User.GetUserByID({'id': session['id']})
    all_sightings = Sasquatch.get_all_sightings()
    
    return render_template('dashboard.html', user=user, all_sightings = all_sightings)


# DIRECTS USER TO NEWSHOW.HTML TO ADD NEW SHOW
@app.route('/newSighting/form/')
def newSightingForm():
    if "id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')
    user = User.GetUserByID({'id': session['id']})
    return render_template('newSighting.html', user=user)

#CREATE A NEW SHOW
@app.route('/addSighting', methods=['POST'])
def addNewSighting():
    if "id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')
    Sasquatch.addSighting(request.form)
    return redirect('/dashboard')

# Direct user to edit show form
@app.route('/editSighting/<int:id>')
def editSightingForm(id):
    if "id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')
    sighting = Sasquatch.get_one_sighting_info({"id":id})
    return render_template('editSighting.html', sighting=sighting)


#EDIT A SHOW
@app.route('/editSighting/form/<int:id>', methods = ['POST'])
def editSighting(id):
    if "id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')
    sighting = Sasquatch.get_one_sighting_info(id)
    # DO NOT RETURN RENDER_TEMPLATE ON A POST
    # ONLY REDIRECT
    return render_template("editSighting.html", sighting = sighting)

#SHOW SIGHTINGS
@app.route('/showSighting/<int:id>')
def showSighting(id):
    if "id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')
    sighting = Sasquatch.get_one_sighting_info({"id":id})
    return render_template('show.html', sighting=sighting)


#DELETE SIGHT POST
@app.route('/delete/<int:id>') #<--- Add ID in parameter to target a specific user
def deleteSighting(id): #<--- ADD ID INTO PARAMETER
    print(session)
    if "id" not in session:
        print("HERE---------->")
        return redirect('/') 
    # if getOneSighting == True
        #delete()
    #else: flash(message)
    sighting = Sasquatch.get_one_sighting_info({"id":id})
    # sighting[0]['user.id'] 
    if sighting.user_id == session['id']:
        Sasquatch.delete(id) #<--- Calling the function targeting id
        return redirect('/dashboard')
    else:
        flash("Only owner can delete!")
        return redirect('/dashboard') #<--- TAKES US BACK TO HOMEPAGE






