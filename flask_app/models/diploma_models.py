from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash


class Diploma:
    def __init__(self, data):
        self.diploma = data["diploma"]
        self.program_tittle = data["program_tittle"]
        self.description = data["description"]
        self.institution_id = data["institution_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    #=========================create diploma program=============
    @classmethod
    def create(cls,data):
        query="""
                INSERT INTO diplomas (diploma,program_tittle,description,institution_id)
                VALUE (%(diploma)s,%(program_tittle)s,%(description)s,%(institution_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #========================get diplomas by id inst================
    @classmethod
    def get_by_id(cls,id):
        query="select * from diplomas where institution_id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,id)
        if len(result) <1:
            return False
        else:
            list=[]
            for row in range(0,len(result)):
                list.append(result[row])
                
        return list
    
    #========================= update diplomas for institution =======================
    @classmethod
    def update(cls,data):
        query="""UPDATE diplomas
                SET diploma=%(diploma1)s,program_tittle=%(program_tittle1)s,description=%(description)s
                WHERE institution_id=%(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    #========================= delete diplomas from institution =======================
    @classmethod
    def delete_diploma(cls,data):
        query="""DELETE FROM diplomas
                WHERE institution_id=%(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)


    # =============== VALIDATIONS ================

    @staticmethod
    def validate(data):
            is_valid = True
        # Check the diploma
            if len(data['diploma1']) < 2:
                flash("Diploma is Required !", "error_diploma")
                is_valid = False
            # Check the program_tittle
            if len(data['program_tittle1']) < 2:
                flash("Program_tittle is Required !", "error_program_tittle")
                is_valid = False
            # Check the description
            if len(data['description1']) < 2:
                flash("Description is Required !", "error_description")
                is_valid = False

            return is_valid