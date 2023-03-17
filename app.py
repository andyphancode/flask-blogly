"""Blogly application."""

from flask import Flask, redirect, render_template
from models import db, connect_db, User
from app import *

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'idksecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home():
    return redirect("/users")

@app.route('/users')
def users():

    users=User.query.all()
    return render_template('users.html', users=users)