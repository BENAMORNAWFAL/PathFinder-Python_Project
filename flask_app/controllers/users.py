from flask_app import app, IMAGES_PATH
from flask import render_template,request, redirect, session,flash,url_for
from flask_app.models.images_model import Image
from flask_app.models.user import User
from flask_app.models.address_model import Address
from flask_app.models.institution_model import Institution
from flask_app.models import admin_model
# Set up OpenAI API credentials
import openai
#add Your api key
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import urllib.request
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER='flask_app/static/uploads/'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']=16*1024*1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

#========================Dashboard===========================

@app.route('/')
def index():
    institutions=Institution.get_all_institutions()
    for inst in institutions:
        print('institution==================================',inst)
    if 'user_id' in session:
        user = User.get_by_id({'id':session['user_id']})
        image=IMAGES_PATH+user.image
        return render_template('index.html', users=user,institutions=institutions,image=image)
    else:
        return render_template('index.html',institutions=institutions)
    
    #========================Root profile===========================
    
@app.route('/profile')
def profile():
    institutions=Institution.get_creator_institutions({'id':session['user_id']})
    favory_ins=Institution.show_favories_institutions({'id':session['user_id']})
    user = User.get_by_id({'id':session['user_id']})
    image=IMAGES_PATH+user.image
    print(image)
    return render_template('user_profile.html',user=user,institutions=institutions,image=image,favory_ins=favory_ins)
        
#========================Root===========================
@app.route('/register')
def log_reg():
    return render_template('register.html')

#========================register=========================
@app.route('/users/register', methods=['post'])
def register():
    if not User.validate_user(request.form):
        return redirect('/register')

    
    data={
        **request.form,
        'image':User.validate_image(request.files['file'].filename),
        'password':bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.create_user(data)
    session['user_id']=user_id
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded and displayed below')
    return redirect('/login')


#=======================Login===================
@app.route('/login')
def loginpage():
    return render_template('login.html')

@app.route('/users/login',methods=['POST'])
def login():
    admin = admin_model.Admin.get_by_name({'name': request.form['email']})
    if admin:
        if request.form['password'] == admin.password:
            return redirect('/admin_dashboard')
    user_db = User.get_by_email(request.form)
    if not user_db:
        flash('Invalid email or password',"login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user_db.password, request.form['password']):
        flash('Invalid email or password',"login")
        return redirect('/login')
    session['user_id']=user_db.id
    
    return redirect('/')
#=======================Edit profile===================
@app.route('/profile/edit')
def edit_profile():
    if 'user_id' not in session:
        return redirect('/') 
    user = User.get_by_id({'id':session['user_id']})
    image=IMAGES_PATH+user.image
    return render_template("edit_profile.html",  user = user,image=image)


@app.route('/profile/update',methods=['post'])
def update_profile():
    data={
        **request.form,
        'image':User.validate_image(request.files['file'].filename)
    }
    if not User.validate_user_edit(request.form):
        return redirect("/profile/edit")
    x= User.update_profile(data)
    
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded and displayed below')
    print("++--"*30,x,"++--"*30)
    return redirect('/profile')

#=======================logout===================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


                                    # OpenAI's API
@app.route("/api", methods=["POST"])
def api():
    # Get the message from the POST request
    message = request.json.get("message")
    
    # Send the message to OpenAI's API and receive the response
    completion = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=200,
        temperature=0.5,
        top_p=1,


    )
    
    # Extract the generated response from the API response
    response = completion.choices[0].text.strip()

    if response:
        return {"content": response}
    else:
        return {"content": 'Failed to generate response!'}

