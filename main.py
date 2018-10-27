from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy 
import cgi
import flask
from sys import exit


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:code123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '1112842616kk'


    #model class for database
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text(560))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


#Initialize Blog Class
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

    def __repr__(self):
        return '<Blog %r>' % self.title    


    #model class for user(owner/user = author)
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)    
    user_username = db.Column(db.String(120))
    user_password = db.Column(db.Text(560))
    user_blogs = db.relationship('Blog', backref='owner')

    #initialize user class for user to have a username and password
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    #string representation of the blog objects
    def __repr__(self):
        return '<User %r>' % self.username


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blog_entry', 'logout']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


#login route handler functions
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        print(user)

        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            no_user = "Sorry you do not have an account, go ahead and create one!" 
            return render_template('signup.html', error=no_user)   

    if request.method == 'GET':
        return render_template('login.html', title='Blogz')


#signup route handler functions
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        
    if username == '':
        no_username = "This field is required please enter!"
        return render_template('signup.html', user_error=no_username)

    if password == '':
        no_password = "This field is required please enter!"
        return render_template('signup.html', password_error=no_password)

    if verify == '': 
        not_verified = "Verify password is required."
        return render_template('singup.html', verify_error=not_verified)

    if password != verify:
        no_match = "Please enter matching passwords."
        return render_template('signup.html', match_error=no_match)

def check_len(input):
    if len(input) >= 8:
        return True
    else:
        return False


def check_special(input):
    specials = 0
    special_list = "! @ $ % ^ & * ( ) _ - + = { } [ ] | \ , . > < / ? ~ ` \" ' : ;".split()
    for char in input:
        if char in special_list:
            specials += 1
    if specials > 0:
        return True
    else:
        return False

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

            if existing_user:
                user_exists = "There is already a user with that name."
                return render_template('signup.html', error=user_exists)

    if request.method == 'GET':
        return render_template('signup.html', title='Blogz')        
 
           
@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
        return redirect('/blog')
    else:
        return redirect('/blog')


  #index route handler functions
@app.route('/', methods=['GET'])  
def index():
    users = User.query.all()
    posts = Blog.query.all()
    return render_template('index.html', title='Blogz', users=users, posts=posts)


#new_posts route handler functions
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'GET':
        return render_template('new_posts.html', title='Blogz')


@app.route('/blogs')
def single_User():


#blog_entry route handler functions
@app.route('/blog', methods=['POST','GET'])
def blog_entry():

    if request.method == 'GET':
        post_id = request.args.get('id')

        if type(post_id) == str:
            posts = Blog.query.get(post_id)
            return render_template('view_post.html', title='Blog post #'+ str(post_id),
                                    posts=posts)
        else:
            posts = Blog.query.all()
            return render_template('blog_entry.html', title='Build a Blog App',
                                        posts=posts)

    if request.method == 'POST':
        post_title = request.form['post-title']
        post_body = request.form['post-body']

        if post_title == '':
            title_error = title_error = 'Please fill in the title'
        else:
            title_error = ''
        if post_body == '':
            body_error = 'Please fill in the body'
        else:
            body_error = ''

        if title_error == '' and body_error == '':

            new_post = Blog(post_title, post_body)
            db.session.add(new_post)
            db.session.commit()
            id= str(new_post.id)
            return redirect('/blog?id=' + id)

        else:
            return render_template('new_posts.html', title_error=title_error, body_error=body_error)

#app shieled by if name main function
if __name__ == '__main__':
    app.run()