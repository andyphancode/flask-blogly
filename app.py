"""Blogly application."""

from flask import Flask, redirect, render_template, request
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

    "Redirect to /users"

    return redirect("/users")

@app.route('/users')
def users():

    "Render a list of users registered"

    users=User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=["GET"])
def add_users():    

    "Render form for adding a new user, ordered by last name alphabetically"

    return render_template('form.html')

@app.route('/users/new', methods=["POST"])
def add_user_submit():

    "Add a new user and return back to home"

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<user_id>')
def show_user(user_id):
    
    "Return details of a user."

    user = User.query.get_or_404(user_id)

    return render_template("detail.html", user=user)

@app.route('/users/<user_id>/edit', methods=["GET"])
def edit_form(user_id):

    "Return form for editing a user's details."

    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route('/users/<user_id>/edit', methods=["POST"])
def edit_user(user_id):

    "Process editing of a user, redirect to home after."

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")
    


@app.route('/users/<user_id>/delete', methods=["POST"])
def delete_user(user_id):

    "Delete a user."

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    users=User.query.all()

    return render_template("users.html", users=users)