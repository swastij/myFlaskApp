from flask import Flask  #flaskblog is a package now
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager


app=Flask(__name__, template_folder='template')     #instance of flask app is created
app.config['SECRET_KEY']= '71e8b3b0948b429cabacb58ba5d8c3f9'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt= Bcrypt(app) #initializing app with bcypt , pw hashing is done in register route
login_manager= LoginManager(app)
login_manager.login_view='login' #redirects to login if user is not logged in and accesses login_required field
login_manager.login_message_category='info' #info is a bootstrap class which gives blue alert

from flaskblog import routes #to prevent circular import, we write it after instantiation of app and db