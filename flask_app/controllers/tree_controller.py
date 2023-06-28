from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User
from flask_app.models.tree_model import Tree
bcrypt = Bcrypt(app)


#DASHBOARD
@app.route('/dashboard') 
def loginSuccess():
    if "id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')  #<--- be on every route except the "/" route.
    user = User.GetUserByID({'id': session['id']})
    all_trees = Tree.get_all_trees()
    
    return render_template('dashboard.html', user=user, all_trees = all_trees)


# DIRECTS USER TO NEWSHOW.HTML TO ADD NEW SHOW
@app.route('/newTree/form/')
def newTreeForm():
    if "id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')
    user = User.GetUserByID({'id': session['id']})
    return render_template('newTree.html', user=user)

#CREATE A NEW TREE
@app.route('/addTree', methods=['POST'])
def addNewTree():
    if "id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')
    if not Tree.validate_tree(request.form):
        return redirect('/newTree/form/')
    Tree.addTree(request.form)
    return redirect('/dashboard')

# Direct user to edit tree form
@app.route('/editTree/<int:id>')
def editTreeForm(id):
    if "id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')
    user = User.GetUserByID({"id":session['id']})
    tree = Tree.get_one_tree_info({"id":id})
    return render_template('editTree.html', tree=tree, user=user)


#EDIT A TREE
@app.route('/editTree/form/<int:id>', methods = ['POST'])
def editTree(id):
    if "id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')
    if not Tree.validate_tree(request.form):
        return redirect(f'/editTree/{id}')

    Tree.update(request.form)
    # DO NOT RETURN RENDER_TEMPLATE ON A POST
    # ONLY REDIRECT
    return redirect("/dashboard")

#SHOW TREE INFO
@app.route('/showTree/<int:id>')
def showTreeInfo(id):
    if "id" not in session:
        flash("PLEASE LOGIN!")
        return redirect('/')
    user = User.GetUserByID({"id":session['id']})
    tree = Tree.get_one_tree_info({"id":id})
    return render_template('show.html', user = user,tree=tree)


#DELETE TREE INFO
@app.route('/delete/<int:id>') #<--- Add ID in parameter to target a specific user
def deleteTreeInfo(id): #<--- ADD ID INTO PARAMETER
    print(session)
    if "id" not in session:
        print("HERE---------->")
        return redirect('/') 
    # if getOneSighting == True
        #delete()
    #else: flash(message)
    tree = Tree.get_one_tree_info({"id":id})
    # sighting[0]['user.id'] 
    if tree.users_id == session['id']:
        Tree.delete(id) #<--- Calling the function targeting id
        return redirect('/dashboard')
    else:
        flash("Only owner can delete!")
        return redirect('/dashboard') #<--- TAKES US BACK TO HOMEPAGE
    










