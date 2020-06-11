import secrets
import os
from PIL import Image
from flask import render_template ,url_for,flash ,redirect, request #url_for is used to find route to connect , here used for main.css; flash is used for alert msg, redirect used for redirecting to another page
from flaskblog import app, db, bcrypt # @app.route is using app
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User,Post
from flask_login import login_user, current_user, logout_user, login_required #current_user tells if the user is logged in 

post=[
    {'author':'Swasti Jain',
    'title':'BTS',
    'date_posted':'31 May 2020',
    'content':'I love BTS'
    },
    {'author':'Manvi Jain',
    'title':'Doggo',
    'date_posted':'31 May 2020',
    'content':'I love Doggos'
    }
]

@app.route('/')        
@app.route('/home')
def home():
    return render_template('home.html', posts=post)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/register',methods=['GET','POST']) #to accept get n post requests; methods is a list of allowed methods 
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8') #decode('utf-8) converts the generted pw in bytes into string
        user= User(username=form.username.data, email= form.email.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now login ', 'success') #success is a bootstrap method for alert
        return redirect(url_for('login'))  #if valid form is submitted, redirect to login page
    return render_template('register.html', title='register', form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= LoginForm()
    if form.validate_on_submit():   #valid useremail and pw
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember)
            next_page=request.args.get('next') #next field is present in the url when we are sent to another page when requested other
            return redirect(next_page) if next_page else redirect(url_for('home')) #for redirecting to the page requested initially before asked to login ; so after login we'll get the page requested 
        else:
            flash('Login Unsuccessful! Please check email and password')
    
    return render_template('login.html',title='Login',form=form)      

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))  

def save_picture(form_picture):
    random_hex= secrets.token_hex(8) #we are changing name to avoid collision b/e already existing and new img
    _, f_ext= os.path.splitext(form_picture.filename) #to split and store picture filename and extension
    picture_fn= random_hex + f_ext
    picture_path= os.path.join(app.root_path, 'static/profile_pics',picture_fn) #app.root_path will give path upto current irectory ie flaskblog
    
    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size) #to resize images
    i.save(picture_path)
    
    return picture_fn

@app.route('/account',methods=['GET','POST'])
@login_required  #to redirect to login of not logged in, go to init to understand
def account():
    form= UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file= save_picture(form.picture.data)
            current_user.image_file= picture_file
        current_user.username= form.username.data
        current_user.email= form.email.data
        db.session.commit()
        flash('your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method=='GET': #to populate the form with current user's info
        form.username.data=current_user.username
        form.email.data=current_user.email


    image_file= url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Account', image_file=image_file, form=form)