from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# the regex module
import re 
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Shows:
    DB = "tv_shows_schema"  

    def __init__(self, data): #<---- THIS IS THE OBJECT
        self.show_id = data['show_id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['USER_id']

    @staticmethod       
    def validate_show(show):
        is_valid = True # we assume this is true
        if len(show['title']) < 3:
            flash("Title must be at least 3 characters.")
            is_valid = False
        if len(show['network']) < 3:
            flash("Network must be at least 3 characters.")
            is_valid = False
        if len(show['description']) < 3:
            flash("Description must be at least 3 characters or more.")
            is_valid = False
        return is_valid

    @classmethod
    def addShow(cls, data):
        query = """
        INSERT INTO shows (title, network, release_date, description, USER_id)
        VALUES (%(title)s,%(network)s,%(release_date)s,%(description)s,%(ID)s);
        """
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod #<--- EDIT SHOW
    def GetShowByID(cls, data):
        query = """SELECT * FROM shows 
        WHERE show_id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod #<------ GET ALL
    def get_all_shows(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL(cls.DB).query_db(query)
        shows = []
        for s in results:
            shows.append(cls(s))
        return shows
    
    
    @classmethod #<---- GET ONE METHOD
    def get_one_show_info(cls, show_id):
        query = """
        SELECT * FROM shows
        LEFT JOIN users ON users.user_id = USER_id
        WHERE shows.show_id = %(id)s 
        """
        data = {'id': show_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
