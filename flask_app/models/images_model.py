
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app,DATABASE,IMAGES_PATH
from flask import flash
from flask import render_template,request, redirect, session,flash,url_for


class Image:
    def __init__(self, data):
        self.id = data["id"]
        self.name =IMAGES_PATH+data["name_image"]
        self.institution_id = data["institution_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    #=================create images for institutions ===============
    @classmethod
    def create(cls, data):
        query = """ 
                    INSERT INTO images (institution_id,name_image)
                    VALUES (%(institution_id)s,%(name_image)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)
    #  #========================get images by id inst================
    # @classmethod
    # def get_by_id(cls,id):
    #     query="select * from images where institution_id=%(id)s"
    #     result= connectToMySQL(DATABASE).query_db(query,id)
    #     if len(result)<1:
    #         return False
    #     return result[0]
    
    
    #=================get all images for institutions ===============
    @classmethod
    def get_images_institution(cls,data):
        query = """ 
                    SELECT * FROM images WHERE institution_id =%(institution_id)s;
                """
        results = connectToMySQL(DATABASE).query_db(query,data)
        images = []
        for row in results:
            images.append(cls(row))
        return images
     #========================= update image institution =======================
    @classmethod
    def update(cls,data):
        query="""UPDATE images
                SET name_image=%(files)s
                WHERE institution_id=%(id)s;
                """
        print('query update image 😎😎😎😎😎',query)
        return connectToMySQL(DATABASE).query_db(query, data)
    #========================= delete image institution =======================
    
        #========================= delete image institution =======================
    @classmethod
    def delete_img_inst(cls,data):
        query="""DELETE FROM images
                WHERE institution_id=%(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
            #========================= delete user image  =======================
    @classmethod
    def delete_img_user(cls,data):
        query="""DELETE FROM images
                WHERE user_id=%(id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result
    #=============================validate image========================
    @staticmethod
    def validate_image(data):
        if data=='' :
            img='user-circle-light.png'
        else:
            img=data
        return img