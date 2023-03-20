"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post, Tag, PostTag
from app import *

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'idksecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.errorhandler(404)
def error_age():
    """404 Page"""

    return render_template('404.html'), 404

@app.route('/')
def home():
    """Show 5 recent posts"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("home.html", posts=posts)

@app.route('/users', methods=["GET"])
def users():
    """Render a list of users registered"""

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
def show_user_details(user_id):
    "Return details of a user."
    
    user = User.query.get_or_404(user_id)

    return render_template("detail.html", user=user)

@app.route('/users/<user_id>/edit', methods=["GET"])
def show_edit_user_form(user_id):
    "Return form for editing a user's details."

    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route('/users/<user_id>/edit', methods=["POST"])
def edit_user(user_id):
    "Process editing of a user, redirect to user list after."

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")
    


@app.route('/users/<user_id>/delete', methods=["POST"])
def delete_user(user_id):
    "Delete a user and redirect to user list."

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<user_id>/posts/new', methods=["GET"])
def show_add_post_form(user_id):
    """Render template for adding post."""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('post_form.html', user=user, tags=tags)

@app.route('/users/<user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Handle adding a post."""

    user = User.query.get_or_404(user_id)

    tags = Tag.query.filter(Tag.id.in_([int(num) for num in request.form.getlist("tags")])).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<post_id>', methods=["GET"])
def show_post_details(post_id):
    """Show post details."""

    post = Post.query.get_or_404(post_id)
    

    return render_template("post.html", post=post)

@app.route('/posts/<post_id>/edit', methods=["GET"])
def show_edit_post_form(post_id):
    """Show form for editing post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("post_edit.html", post=post, tags=tags)

@app.route('/posts/<post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Edit a post and redirect to post detail page."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    post.tags = Tag.query.filter(Tag.id.in_([int(num) for num in request.form.getlist("tags")])).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route('/posts/<post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete a post and redirect to user detail page."""

    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/tags', methods=["GET"])
def show_tags():

    tags = Tag.query.all()

    return render_template("taglist.html", tags=tags)

@app.route('/tags/new', methods=["GET"])
def show_new_tag_form():

    return render_template("tagnew.html")

@app.route('/tags/new', methods=["POST"])
def add_new_tag():

    tag = Tag(name=request.form['name'])

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<tag_id>', methods=["GET"])
def show_tag_details(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    return render_template("tagposts.html", tag=tag)

@app.route('/tags/<tag_id>/edit', methods=["GET"])
def show_edit_tag_form(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    return render_template("tagedit.html", tag=tag)

@app.route('/tags/<tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')