from flask_app import app,IMAGES_PATH
from flask import  render_template,request, redirect, session
from flask_app.models.comment import Comment
from flask_app.models.institution_model import Institution
from flask_app.models.address_model import Address
from flask_app.models.user import User
from flask_app.models.review import Review
from flask_app.models.images_model import Image
from flask_app.models.favory_model import Favory
from flask_app.models.diploma_models import Diploma
from flask_app.models.admin_model import Admin


# =================== index =====================
# @app.route("/aaa")
# def index2():
    
#     return redirect("/admin")


# =================== show admin dashboard =====================
@app.route("/admin_dashboard")
def dashboard_admin():
    
    users = User.get_all_users()
    total_users = len(users)
    creators = User.get_all_creators()
    creators = len(creators)
    comments = Comment.count_all_comment()
    tday_comments = Comment.get_all_today_comments()
    institutions = Institution.get_awaiting_institutions()
    return render_template("dashboard_admin.html",institutions=institutions,total_users=total_users,creators=creators,comments=comments,tday_comments=tday_comments)


# =================== list users =====================
@app.route("/list_users")
def list_users():

    users=User.get_all_users()
    return render_template('user_list.html',users=users)

# =================== list users =====================
@app.route("/list_creators")
def list_creators():
    users=User.get_all_creators()
    return render_template('creator_list.html',creators=users)

# =================== accept institution =====================
@app.route("/accept/<int:id>")
def accept(id):
    Institution.accept({"id": id})
    return redirect("/admin_dashboard")

# =================== reject institution =====================
@app.route("/reject/<int:id>")
def reject(id):
    Image.delete_img_inst({'id':id})
    Diploma.delete_diploma({'id':id})
    Address.delete_adresse({'id':id})
    Institution.delete_institution({"id": id})
    return redirect("/admin_dashboard")
# =================== delete user =====================
@app.route("/delete/<int:id>")
def delete_user(id):

    
    # results = Institution.get_by_id_creator({"id": id})
    # for result in results:
    #         Review.delete_rate_inst({'id':result.id})
    #         Favory.delete_favory_inst({'id':result.id})
    #         Comment.delete_comment_inst({'id':result.id})
    #         Image.delete_img_inst({'id':result.id})
    #         Diploma.delete_diploma({'id':result.id})
    #         Address.delete_adresse({'id':result.id})
    # Institution.delete_institution_by_user_id({"id": id})
    
    Favory.delete_favory_user({'id':id})
    Comment.delete_comment_user({'id':id})
    Image.delete_img_user({'id':id})
    User.delete({'id':id})
    return redirect('/list_users')
# =================== delete creator =====================
@app.route("/delete_creator/<int:id>")
def delete_creators(id):
    Favory.delete_favory_user({'id':id})
    Comment.delete_comment_user({'id':id})
    Image.delete_img_user({'id':id})
    User.delete({'id':id})
    return redirect('/list_creators')