from flask import Flask  #flaskblog is a package now
from flask_sqlalchemy import SQLAlchemy 


app=Flask(__name__, template_folder='template')     #instance of flask app is created
app.config['SECRET_KEY']= '71e8b3b0948b429cabacb58ba5d8c3f9'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

from flaskblog import routes #to prevent circular import, we write it after instantiation of app and db