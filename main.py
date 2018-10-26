from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy 
import cgi
import flask


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:code123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

    #model class for database
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text(560))

    #model class for user
class User(db.Model):
    owner_id = db.Column(db.Integer, primary_key=True)    
    owner_title = db.Column(db.String(120))
    owner_body = db.Column(db.Text(560 ))


    #Initialize Blog Class
    def __init__(self, title, body):
        self.title = title
        self.body = body

    #string representation of the blog objects
    def __repr__(self):
        return '<Blog %r>' % self.name


#signup route handler functions
@app.route('/signup', methods=['POST', 'GET'])
def singleUser(signup):

#login route handler functions
@app.route('/login', methods=['POST', 'GET'])
def login():

#index route handler functions
@app.route('/index', methods=['POST', 'GET'])  
def index():
    if request.method == 'POST':    

#new_posts route handler functions
@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'GET':
        return render_template('new_posts.html', title='Add Blog Entry')

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