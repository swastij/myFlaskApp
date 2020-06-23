from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app #app is used for secret key;__main__ is replaced because flaskblog will not be called __main__ but it db will be accessed through __init__ now
from flask_login import UserMixin

@login_manager.user_loader  #login extension needs this decorator to load/find user through user_id, it is necessity for its proper working
def load_user(user_id):
    return User.query.get(int(user_id)) #typecasted just to be sure

class User(db.Model, UserMixin):        #inheriting db.Model
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(20), nullable=False)
    image_file=db.Column(db.String(20), nullable=False, default='default.jpg')
    posts=db.relationship('Post', backref='author', lazy=True ) #referencing Post class
    #setting relation with Post, author is an attribute used to know the user who created the post, lazy=TRue will make db know that this data is necessary to load

    def get_reset_token(self, expires_sec=1800):
        print("reset token")
        s= Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8') #s.dumps will create a token, user_id is payload here

    @staticmethod               #nothing is done with instances , self is not passed as argument
    def verify_token(token):
        s= Serializer(app.config['SECRET_KEY'])
        #exception may be due to invallid token / timeout
        try:
            user_id = s.loads(token)['user_id'] #this user_id will be passed through get_reset_token
        except:
            return None
        return User.query.get(user_id)

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