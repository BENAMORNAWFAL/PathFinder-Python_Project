from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Review:
    # CONSTRUCTOR - Make Defaults
    def __init__(self, data):
        self.id = data["id"]
        self.rate = data["rate"]
        self.user_id = data["user_id"]
        self.institution_id = data["institution_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # ========== CREATE review ============
    @classmethod
    def create(cls, data):
        query = """ 
                    INSERT INTO reviews (rate, user_id, institution_id)
                    VALUES (%(rate)s,  %(user_id)s, %(institution_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)

    # ========= check review by ID ============
    @classmethod
    def check_review(cls, data):
        query  = """SELECT * FROM reviews 
        WHERE user_id = %(user_id)s AND institution_id = %(institution_id)s;"""
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results :
            return False
        return cls(results[0])
    
    # ========= GET reviews by institution_id ============
    @classmethod
    def get_by_id(cls, data):
        query  = """select * from reviews
                    where institution_id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db(query, data)
        reviews = []
        for result in results:
            reviews.append(cls(result))
        return reviews
         #========================= delete review institution =======================
    @classmethod
    def delete_rate_inst(cls,data):
        query="""DELETE FROM reviews
                WHERE institution_id=%(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # ========= Calculate the institution reviews rate ============
    def total_rate(data):
        sum = 0
        if data == []: 
            return sum
        for row in data:
            sum += row.rate
        rate = sum / len(data)
        return rate