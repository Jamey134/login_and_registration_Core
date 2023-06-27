from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# the regex module
import re 
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User: #<----- MODEL CLASS
    #"DB" TO STORE MYSQL SCHEMA
    DB = "sasquatch_schema"  #<----- CREATE VARIABLE 

    def __init__(self, data): #<---- INITIATE FUNCTION TO CREATE THE OBJECT AND VAIDATES THE USER.
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']#<---- KEYS AMD VALUES MUST MATCH WHAT'S IN MYSQL
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
        if len(user['password']) < 4:
            flash("Password must be at least 4 characters or more.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Please enter valid email address.")
        if user['password'] != ['confirm_password']:
            flash('Password did not match.')
        return is_valid
    
    @staticmethod  
    def validateUpdate(user): #<--- USED FOR VALIDATING USER IN ORDER TO UPDATE INFO
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        return is_valid
    
    @classmethod  #<--------- CREATE FUNCTION
    def create(cls, data):
        query = """
    INSERT INTO users (first_name,last_name,email,password)
    VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
    """
        print('here', data)
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod    #<----- GET ALL METHOD (READ)
    def get_all(cls): #<----- ONLY ADD CLASS IN PARAMETER
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = [] #<--- CREATE VARIABLE WITH EMPTY LIST TO RETURN REQUESTED DATA 
        for u in results:
            users.append(cls(u))
        return users
    

    
    @classmethod  #<----- GET ONE METHOD (BY ID)(READ)
    def GetUserByID(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @classmethod  #<----- GET ONE METHOD (BY EMAIL)(READ)
    def GetUserByEmail(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results) #<---- USED FOR TESTING MY FUNCTION
        return cls(results[0])
    
    @classmethod #<-----UPDATE FUNCTION
    def edit(cls, data): 
        query = """UPDATE users 
                SET first_name=%(first_name)s,last_name=%(last_name)s 
                WHERE id = %(id)s;
                """
        print("HERE------->", data)
        return connectToMySQL(cls.DB).query_db(query,data)
    
    # the delete method will be used when we need to delete an user from our database
    # @classmethod #<----- DELETE METHOD
    # def delete(cls, user_id): #<---- ADD CLASS AND ID INTO PARAMETER
    #     query  = """DELETE FROM users 
    #     WHERE id = %(id)s;
    #     """ #<--- THIS WILL DELETE ENTIRE ROW BY SELECTING ID
    #     data = {"id": id}
    #     return connectToMySQL(cls.DB).query_db(query, data)
    

