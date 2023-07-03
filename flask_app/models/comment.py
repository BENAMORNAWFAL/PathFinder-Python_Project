from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE


class Comment:
    # CONSTRUCTOR - Make Defaults
    def __init__(self, data):
        self.id = data["id"]
        self.comment = data["comment"]
        self.user_id = data["users_id"]
        self.institution_id = data["institutions_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.full_name = None

    # ========== CREATE new comment ============
    @classmethod
    def create(cls, data):
        query = """ 
                    INSERT INTO comments (comment,users_id, institutions_id)
                    VALUES (%(comment)s,%(user_id)s,  %(institution_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)
      #========================= delete comment institution =======================
    @classmethod
    def delete_comment_inst(cls,data):
        query="""DELETE FROM comments
                WHERE institutions_id=%(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
        #========================= delete user comment =======================
    @classmethod
    def delete_comment_user(cls,data):
        query="""DELETE FROM comments
                WHERE users_id=%(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
    # ========= show favory by ID ============
    @classmethod
    def get_all_comments(cls, data):
        query  = """SELECT * FROM comments join users on comments.users_id = users.id
        WHERE institutions_id = %(institution_id)s;"""
        results = connectToMySQL(DATABASE).query_db(query, data)
        list = []
        if not results:
            return list
        for result in results:
            comment = cls(result)
            comment.full_name = result['first_name'] +" "+ result['last_name']
            list.append(comment)
        return list
    
     # ========= get all comments number ============
    @classmethod
    def count_all_comment(cls):
        query  = """SELECT count(id) as count FROM comments;"""
        results = connectToMySQL(DATABASE).query_db(query)
        return results[0]['count']
    
    # ========= get all today comments ============
    @classmethod
    def get_all_today_comments(cls):
        query  = """SELECT count(id) as count FROM comments where date(created_at) = CURRENT_DATE();"""
        results = connectToMySQL(DATABASE).query_db(query)
        return results[0]['count']

