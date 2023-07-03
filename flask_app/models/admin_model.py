from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Admin:
    def __init__(self,data):
        self.id=data['id']
        self.name=data['name']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        
    
    #=========================get admin by name=====================
    @classmethod
    def get_by_name(cls, data):
        query="select * from admins WHERE name=%(name)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)
        if not result:
            return False
        return cls(result[0])
    