from datetime import datetime
from flask import Flask, render_template ,url_for, flash, redirect  #url_for is used to find route to connect , here used for main.css; flash is used for alert msg, redirect used for redirecting to another page
from flask_sqlalchemy import SQLAlchemy 
from forms import RegistrationForm, LoginForm

app=Flask(__name__, template_folder='template')     #instance of flask app is created
app.config['SECRET_KEY']= '71e8b3b0948b429cabacb58ba5d8c3f9'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

db.create_all()
db.session.commit()

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
    
    def __repr__(self):     #magic fxn
        return f"Post ('{self.title}','{self.date_posted}') "

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
#db.create_all()
#db.session.commit()
# user = User(username="test1",  email="test1@abc.com", password="test", image_file="asd")
# db.session.add(user)
# db.session.commit()

users = User.query.all()
for u in users:
    print(u)

@app.route('/')        
@app.route('/home')
def home():
    return render_template('home.html',sposts=post)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/register',methods=['GET','POST'])
def register():
    form= RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success') #success is a bootstrap method for alert
        return redirect(url_for('home'))  #if valid form is submitted, redirect to home page
    return render_template('register.html', title='register', form=form)

@app.route('/login')
def login():
    form= LoginForm()
    return render_template('login.html', title='login', form=form)


if __name__ == "__main__":
    app.run(debug='True')   #if we remove debug part, we'll have to restart again to reload, debug will show changes with just reload