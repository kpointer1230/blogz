from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy 
import cgi
import flask


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Ktp1206@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

    #model class for database
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db, String(120))
    body = db.Column(db.Text(560))

    #Initialize Blog Class
    def __init__(self, title, body):
        self.title = title
        self.body = body

    #string representation of the blog objects
    def __repr__(self):
        return '<Blog %r>' % self.name



