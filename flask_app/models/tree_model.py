from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model
# the regex module
import re 
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Tree:
    DB = "arbortrary_schema"  

    def __init__(self, data): #<---- THIS IS THE OBJECT
        self.id = data['id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.date_planted = data['date_planted']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']

    @staticmethod       
    def validate_tree(tree):
        is_valid = True # we assume this is true
        if len(tree['species']) < 5:
            flash("Species must be at least 5 characters.")
            is_valid = False
        if len(tree['location']) < 2:
            flash("Location of tree must be at least 2 characters.")
            is_valid = False
        if len(tree['reason']) < 50:
            flash("Reason must be at least 50 characters.")
            is_valid = False
        return is_valid

    @classmethod
    def GetSightingByID(cls, data):
        query = """SELECT * FROM sightings
        WHERE id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod   #<----- Create Tree Entry
    def addTree(cls, data):
        query = """
        INSERT INTO trees (species, location, reason, date_planted,users_id)
        VALUES (%(species)s,%(location)s,%(reason)s,%(date_planted)s,%(users_id)s);
        """
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    # @classmethod #<--- EDIT SHOW
    # def GetShowByID(cls, data):
    #     query = """SELECT * FROM shows 
    #     WHERE show_id = %(id)s;
    #     """
    #     results = connectToMySQL(cls.DB).query_db(query, data)
    #     return results
    
    @classmethod #<------ GET ALL
    def get_all_trees(cls):
        query = """SELECT * FROM trees
            LEFT JOIN users ON users.id = trees.users_id;"""
        results = connectToMySQL(cls.DB).query_db(query)
        trees = []
        for row in results:
            one_tree=cls(row)
            userData = {
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at']
            }
            
            one_tree.reporter = user_model.User(userData)
            trees.append(one_tree)
        return trees
    
    @classmethod #<---- Edit Tree Information
    def update(cls, data):
        query = """
            UPDATE trees
            SET species = %(species)s, 
            location = %(location)s, 
            reason = %(reason)s, 
            date_planted = %(date_planted)s
            WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)


    @classmethod #<---- GET ONE METHOD (USE FOR DISPLAYING INFO)
    def get_one_tree_info(cls, data):
        query = """
        SELECT * FROM trees
        LEFT JOIN users ON users.id = trees.users_id
        WHERE trees.id = %(id)s 
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        one_tree = cls(results[0])
        userData = {
            "id" : results[0]['users.id'],
            "first_name" : results[0]['first_name'],
            "last_name" : results[0]['last_name'],
            "email" : results[0]['email'],
            "password" : results[0]['password'],
            "created_at" : results[0]['users.created_at'],
            "updated_at" : results[0]['users.updated_at']
        }
        #creating a new attribute called "reporter" where we are storing the user's information inside it.
        one_tree.reporter = user_model.User(userData)
        return one_tree
    

    @classmethod #<----- DELETE METHOD
    def delete(cls, id): #<---- ADD CLASS AND ID INTO PARAMETER
        query  = """DELETE FROM trees 
        WHERE id = %(id)s;
        """ #<--- THIS WILL DELETE ENTIRE ROW BY SELECTING ID
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query, data)
    
@classmethod
def get_user_with_trees( cls , data ):
        query = """SELECT *
                FROM users
                JOIN trees
                ON users.id = trees.users_id
                WHERE users.id = %(user_id)s;
        """
        result = connectToMySQL(cls.DB).query_db( query , data )

        one_user = cls(result[0])
        
        for row in result:

            tree_data = {
                "id" : row['id'],
                "species" : row['species'],
                "location" : row['location'],
                "reason" : row['reason'],
                "date_planted" : row['date_planted'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
                "users_id" : row['users_id']
            }
        
        one_user.trees.append(tree_model.Tree(tree_data))

        return one_user
    