from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# the regex module
import re 
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Shows:
    DB = "tv_shows_schema"  

    def __init__(self, data):
        self.show_id = data['show_id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

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
        INSERT INTO shows (title, network, release_date, description)
        VALUES (%(title)s,%(network)s,%(release_date)s,%(description)s);
        """
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def GetShowByID(cls, data):
        query = "SELECT * FROM shows WHERE show_id = %(show_id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def get_all_shows(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL(cls.DB).query_db(query)
        shows = []
        for s in results:
            shows.append(cls(s))
        return shows
    
    @classmethod
    def viewShow(show_id):
        query = 
