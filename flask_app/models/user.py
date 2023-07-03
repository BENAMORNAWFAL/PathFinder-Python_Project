from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re	  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.is_creator=data['is_creator']
        self.image=data['image']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        

    
    #=========================create user============================
    @classmethod
    def create_user(cls, data):
        
        query = """INSERT INTO users (first_name, last_name, email, password,is_creator,image)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(is_creator)s,%(image)s);"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #=========================get user par email=====================
    @classmethod
    def get_by_email(cls, data):
        query="select * from users WHERE email=%(email)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result) <1:
            return False
        return cls(result[0])
    
    #=========================get user by id=======================
    @classmethod
    def get_by_id(cls, data):
        query="SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        # print(results,"******---"*25)
        if len(results)< 1 :
            return []
        return cls(results[0])
    
    @classmethod
    def get_all_users(cls):
        users =[]
        query = """SELECT * FROM users WHERE is_creator = 0;"""
        results = connectToMySQL(DATABASE).query_db(query)
        for result in results:
            users.append(cls(result))
        print('*'*30,users)
        return users
     # ========= GET all creators ============
    @classmethod
    def get_all_creators(cls):
        users =[]
        query = """SELECT * FROM users WHERE is_creator = 1;"""
        results = connectToMySQL(DATABASE).query_db(query)
        for result in results:
            users.append(cls(result))
        print('*'*30,users)
        return users
    
    #================================ delete user ==============
    @classmethod
    def delete(cls,data):
        query="delete from users where id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
     #=========================get image user=======================
    @classmethod
    def get_image(cls):
        query="SELECT * FROM users;"
        result= connectToMySQL(DATABASE).query_db(query)

        if len(result) <1:
            return False
        return cls(result[0])
    
    @classmethod
    def update_profile(cls, data):
        query = """
            UPDATE users SET first_name =%(first_name)s,last_name =%(last_name)s,image =%(image)s
            WHERE id = %(id)s ;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #=============================validate user========================
    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data['first_name'])<2:
            flash("First Name must be more than 2 characters!","reg_fn")
            is_valid = False
        if len(data['last_name'])<2:
            flash("Last Name must be more than 2 characters!","reg_ln")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Email must be valid !","reg_email")
            is_valid = False
        elif User.get_by_email({'email':data['email']}):
            flash("Email already exist !","reg_email")
            is_valid = False
        if len(data['password'])<8:
            flash("Password must be more than 8 characters!","reg_password")
            is_valid = False
        elif data['password']!=data['confirm_password']:
            flash("Passwords do not match!","reg_password_conf")
            is_valid = False

        return is_valid
    #=============================validate image========================
    @staticmethod
    def validate_user_edit(data):
        is_valid = True

        if len(data['first_name'])<2:
            flash("First Name must be more than 2 characters!","reg_fn")
            is_valid = False
        if len(data['last_name'])<2:
            flash("Last Name must be more than 2 characters!","reg_ln")
            is_valid = False
        return is_valid
    @staticmethod
    def validate_image(data):
        if data=='' :
            img='user-circle-light.png'
        else:
            img=data
        return img
    

