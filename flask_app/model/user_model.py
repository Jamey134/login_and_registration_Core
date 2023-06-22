from flask_app.config.mysqlconnection import connectToMySQL

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


    @classmethod     #<--------- CREATE or EDIT
    def save(cls, data):
        query = """
    INSERT INTO users (first_name,last_name,email,password)
    VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
    """
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod    #<------- GET ALL
    def get_all(cls, data):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for u in results:
            users.append(cls(u))
        return users