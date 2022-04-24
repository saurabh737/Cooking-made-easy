from distutils.log import error
from unicodedata import name
from urllib.parse import uses_relative
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import requests, json
from sympy import primefactors
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from .models import *
# login_manager = LoginManager()
# from flask_session import Session

auth = Blueprint('auth', __name__)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    data = {}
    data['email'] = email
    data['password'] = password
    if request.method == 'POST':
        req = requests.post('http://127.0.0.1:3000/user/login', json = data)
        userData = req.json()
        if req.status_code == 200:
            # User(userData)
            print(session,"=-=-=-=-", userData["name"])
            session["name"] = userData["name"]
            return render_template("getrecipes.html")
        elif req.status_code == 401:
            flash('Incorrect credentials!', category="error")
    return render_template("login.html")

@auth.route('/logout')
def logout():
    flash('Logged Out Successfully', category='success')
    session['name'] = None
    return render_template("home.html")

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    email = request.form.get('email')
    firstName = request.form.get('firstName')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    data = {}

    data['email'] = email
    data['password'] = password1
    data['name'] = firstName
    
    if password1 != password2:
        flash('Passwords dont match', category="error")
    elif request.method == 'POST':
        req = requests.post('http://127.0.0.1:3000/user/signup', json = data)
    
        if req.status_code == 401:
            flash('Email already exists', category="error")
        elif req.status_code == 503:
            flash('Something went wrong!', category="error")
        else:
            flash('Account created!', category='success')
            return render_template("getrecipes.html")

    return render_template("signup.html")

# class User(self, data):
#     name = data.name
#     password = db.StringField()
#     email = db.StringField()
#     def to_json(self):
#         return {"name": self.name,
#                 "email": self.email}
#     def is_authenticated(self):
#         return True
#     def is_active(self):
#         return True
#     def is_anonymous(self):
#         return False
#     def get_id(self):
#         return str(self.id)