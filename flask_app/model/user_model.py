from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class User:
    DB = "login_and_registration_schema"  

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Static methods don't have self or cls passed into the parameters.
    # We do need to take in a parameter to represent our user.
    @staticmethod       
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if len(user['password']) < 6:
            flash("Password must be at least 6 characters.")
            is_valid = False
        return is_valid
    
    
    @classmethod     #<--------- CREATE or EDIT
    def save(cls, data):
        query = """
    INSERT INTO users (first_name,last_name,email,password)
    VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
    """
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod    #<------- GET ALL METHOD
    def get_all(cls, data):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        users = []
        for u in results:
            users.append(cls(u))
        return users
    
    @classmethod     #<----- GET ONE METHOD
    def GetUserByID(cls, data):
        query = """
        SELECT FROM users
        WHERE id = %(id)s
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod       #<----- GET ONE METHOD
    def GetUserByEmail(cls, data):
        query = """
        SELECT FROM users
        WHERE email = %(email)s
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
