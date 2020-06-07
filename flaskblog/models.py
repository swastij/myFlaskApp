from datetime import datetime
from flaskblog import db #__main__ is replaced because flaskblog will not be called __main__ but it db will be accessed through __init__ now


class User(db.Model):        #inheriting db.Model
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(20), nullable=False)
    image_file=db.Column(db.String(20), nullable=False, default='default.jpg')
    posts=db.relationship('Post', backref='author', lazy=True ) #referencing Post class
    #setting relation with Post, author is an attribute used to know the user who created the post, lazy=TRue will make db know that this data is necessary to load

    def __repr__(self):     #magic fxn
        return f"User ('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(20), nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #we passed fxn to default and not called it (utcnow())
    content=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #passing/referencing table name user and column id
    
    def __repr__(self):    
        return f"Post ('{self.title}','{self.date_posted}') "