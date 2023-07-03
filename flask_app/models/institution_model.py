from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app,DATABASE,IMAGES_PATH
from flask_app.models import address_model
from flask import flash
from flask import render_template,request, redirect, session,flash,url_for

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Institution:
    # CONSTRUCTOR - Make Defaults
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.select_inst = data["select_inst"]
        self.email = data["email"]
        self.phone = data["phone"]
        self.fax = data["fax"]
        self.creator_id = data["creator_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # ========== CREATE Institution ============
    @classmethod
    def create(cls, data):
        query = """ 
                    INSERT INTO institutions (name,select_inst, email, phone, fax, creator_id)
                    VALUES (%(name)s,  %(type)s,  %(email)s, %(phone)s,%(fax)s, %(creator_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)


    #=========================get user by id creator =======================
    @classmethod
    def get_by_id_creator(cls,id):
        query="SELECT * FROM institutions join users on users.id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,id)
        # print("slect inst 🐱‍🐉🐱‍🐉🐱‍🐉============================",result)
        if len(result) <1:
            return False
        return result[0]
    
     # ========= GET institutions by ID ============
    @classmethod
    def get_by_id(cls, data):
        query  = """SELECT * FROM institutions WHERE id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db(query, data)
        institution = cls(results[0])
        institution.image = cls.get_image({'institution_id':institution.id})
        return institution
    #=========================get all creators =======================
    @classmethod
    def get_all_institutions(cls):
        query = """
            select * from institutions; 
        """
        results = connectToMySQL(DATABASE).query_db(query)
        # print(results)
        institutions = []
        for row in results:
            institution=cls(row)
            institution.image = cls.get_image({'institution_id':institution.id})
            institutions.append(institution)
        return institutions
    
    #=========================get creator institutions =======================
    @classmethod
    def get_creator_institutions(cls,data):
        query = """
            select * from institutions where institutions.creator_id=%(id)s ; 
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        # print(results)
        institutions = []
        for row in results:
            institution=cls(row)
            institution.image = cls.get_image({'institution_id':institution.id})
            institution.address = address_model.Address.get_by_id({'id':institution.id})
            institutions.append(institution)
        return institutions 
    
    @classmethod
    def get_image(cls,data):
        query = """
        SELECT * FROM images where institution_id = %(institution_id)s order by created_at limit 1;
        """
        result  = connectToMySQL(DATABASE).query_db(query,data)
        if result:
            # print("👌"*20,result[0]['name_image'],"👌"*20)
            return IMAGES_PATH+result[0]['name_image']
        return None
    
    
    #========================= Update institution =======================
    @classmethod
    def update(cls,data):
        query="""UPDATE institutions
                SET select_inst=%(type)s,name=%(name)s,email=%(email)s,phone=%(phone)s,fax=%(fax)s
                WHERE id=%(id)s;
                """
        print('query update institution 😎😎😎😎😎',query)
        return connectToMySQL(DATABASE).query_db(query, data)

    #========================= delete institution =======================
    @classmethod
    def delete_institution(cls,data):
        query="""DELETE FROM institutions
                WHERE id=%(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    
        #========================= delete institution =======================
    @classmethod
    def delete_institution_by_user_id(cls,data):
        query="""DELETE FROM institutions
                WHERE user_id=%(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    

    #========================= show favorite in profile user=======================
    @classmethod
    def show_favories_institutions(cls, data):
        query = """
                    select * from institutions
                    join favorites on favorites.institution_id = institutions.id
                    where user_id =%(id)s;
                """
        institutions =[]
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
                return 0
        for result in results:
            institution=cls(result)
            institution.image = cls.get_image({'institution_id':institution.id})
            institution.address = address_model.Address.get_by_id({'id':institution.id})
            institutions.append(institution)
        return institutions
    # ========= GET institution that is awaiting admin approval ============
    @classmethod
    def get_awaiting_institutions(cls):
        institutions =[]
        query = """SELECT * FROM institutions WHERE is_accept = 0;"""
        results = connectToMySQL(DATABASE).query_db(query)
        if not results:
            return 0
        for result in results:
            institution=cls(result)
            institution.image = cls.get_image({'institution_id':institution.id})
            institution.address = address_model.Address.get_by_id({'id':institution.id})
            institutions.append(institution)
        return institutions
    

    # ========= accept institution by ID ============
    @classmethod
    def accept(cls,data):
        query="""UPDATE institutions
        SET is_accept = 1
        WHERE id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)
    

    # =============== VALIDATIONS ================

    @staticmethod
    def validate(data):
        is_valid = True  # we assume this is true
        # Check the name
        if len(data['name']) < 3:
            flash("Name is Required !", "error_name")
            is_valid = False
        # Check the phone
        if len(data['phone']) < 2:
            flash("Phone is Required !", "error_phone")
            is_valid = False
        # Check the diploma
        # if len(data['diploma']) < 2:
        #     flash("Diploma is Required !", "error_diploma")
        #     is_valid = False
        # Check the program_tittle
        # if len(data['program_tittle']) < 2:
        #     flash("Program_tittle is Required !", "error_program_tittle")
        #     is_valid = False
        # Check the description
        # if len(data['description']) < 2:
        #     flash("Description is Required !", "error_description")
        #     is_valid = False
        # Check the email
        if len(data["email"]) < 1:
            is_valid = False
            flash("Email is Required !", "error_email")
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address!", "error_email")
            is_valid = False

        return is_valid
    @staticmethod
    def validate_institution_image(data):
        if len(data) == 1 :
            data.pop()
            img='img_institution.png'
            data.append({'name_image' : img})
            print('null is true 888888888888888888888888888888')
            return data
        else:
            return data