"""Blogly application."""
from flask import Flask, request, render_template,  redirect, flash, session
from models import db,  connect_db, User
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

db.create_all()

@app.route('/')
def re_route():
    return redirect('/users')

@app.route('/users')
def show_users():
    
    users = User.query.all()
    
    return render_template('userlink.html', users=users)

@app.route('/users/new')
def show_form():
    return render_template('form.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    db.session.add(new_user)
    
    db.session.commit()
    
    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    
    user = User.query.get_or_404(user_id)
    
    return render_template("details.html", user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):


    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")