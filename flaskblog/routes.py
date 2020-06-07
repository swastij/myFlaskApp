from flask import render_template ,url_for, flash, redirect  #url_for is used to find route to connect , here used for main.css; flash is used for alert msg, redirect used for redirecting to another page
from flaskblog import app # @app.route is using app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User,Post

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
