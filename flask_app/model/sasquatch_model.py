from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.model import user_model
# the regex module
import re 
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Sasquatch:
    DB = "sasquatch_schema"  

    def __init__(self, data): #<---- THIS IS THE OBJECT
        self.id = data['id']
        self.location = data['location']
        self.date_of_sighting = data['date_of_sighting']
        self.what_happened = data['what_happened']
        self.num_of_sasquatches = data['num_of_sasquatches']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @staticmethod       
    def validate_sighting(sighting):
        is_valid = True # we assume this is true
        if len(sighting['location']) < 3:
            flash("Location must be at least 3 characters.")
            is_valid = False
        if len(sighting['what_happened']) < 3:
            flash("Description of sighting must be at least 3 characters.")
            is_valid = False
        if len(sighting['num_of_sasquatches']) < 3:
            flash("Min of 1 sasquatch is required.")
            is_valid = False
        return is_valid

    @classmethod
    def GetSightingByID(cls, data):
        query = """SELECT * FROM sightings
        WHERE id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod   #<----- Create show
    def addSighting(cls, data):
        query = """
        INSERT INTO sightings (location, date_of_sighting, what_happened, num_of_sasquatches,user_id)
        VALUES (%(location)s,%(date_of_sighting)s,%(what_happened)s,%(num_of_sasquatches)s,%(user_id)s);
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
    def get_all_sightings(cls):
        query = """SELECT * FROM sightings
            LEFT JOIN users ON users.id = sightings.user_id;"""
        results = connectToMySQL(cls.DB).query_db(query)
        sightings = []
        for row in results:
            one_sighting=cls(row)
            userData = {
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at']
            }
            
            one_sighting.reporter = user_model.User(userData)
            sightings.append(one_sighting)
        return sightings
    
    
    @classmethod #<---- GET ONE METHOD (USE FOR DISPLAYING INFO)
    def get_one_sighting_info(cls, data):
        query = """
        SELECT * FROM sightings
        LEFT JOIN users ON users.id = sightings.user_id
        WHERE sightings.id = %(id)s 
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        one_sighting = cls(results[0])
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
        one_sighting.reporter = user_model.User(userData)
        return one_sighting
    

    @classmethod #<----- DELETE METHOD
    def delete(cls, id): #<---- ADD CLASS AND ID INTO PARAMETER
        query  = """DELETE FROM sightings 
        WHERE id = %(id)s;
        """ #<--- THIS WILL DELETE ENTIRE ROW BY SELECTING ID
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query, data)
    
