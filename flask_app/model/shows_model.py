from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# the regex module
import re 
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Shows:
    DB = "tv_shows_schema"  

    def __init__(self, data):
        self.show_id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def inside(cls, data):
        query = "SELECT * FROM users WHERE user_id = %(id)s;"
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
    
