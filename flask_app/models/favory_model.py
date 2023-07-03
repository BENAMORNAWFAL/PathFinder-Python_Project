from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE


class Favory:
    # CONSTRUCTOR - Make Defaults
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.institution_id = data["institution_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # ========== CREATE favory ============
    @classmethod
    def create(cls, data):
        query = """ 
                    INSERT INTO favorites (user_id, institution_id)
                    VALUES (%(user_id)s,  %(institution_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)
      #========================= delete favory institution =======================
    @classmethod
    def delete_favory_inst(cls,data):
        query="""DELETE FROM favorites
                WHERE institution_id=%(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
         #========================= delete favory user =======================
    @classmethod
    def delete_favory_user(cls,data):
        query="""DELETE FROM favorites
                WHERE user_id=%(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
        # ========= check favory by ID ============
    @classmethod
    def check_favory(cls, data):
        query  = """SELECT * FROM favorites 
        WHERE user_id = %(user_id)s AND institution_id = %(institution_id)s;"""
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results :
            return False
        return cls(results[0])
    
