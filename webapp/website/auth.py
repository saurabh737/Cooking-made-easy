from distutils.log import error
from unicodedata import name
from urllib.parse import uses_relative
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import requests
from .models import *


auth = Blueprint('auth', __name__)


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
            session["user_id"] = userData["user_id"]
            return redirect(url_for('views.getrecipes'))
        elif req.status_code == 401:
            flash('Incorrect credentials!', category="error")
        elif req.status_code == 403:
            flash('Email ID not found! Please create a new account!', category="error")
    return render_template("login.html")

@auth.route('/logout')
def logout():
    flash('Logged Out Successfully', category='success')
    session['name'] = None
    session["user_id"] = None
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
        userData = req.json()

        if req.status_code == 401:
            flash('Email already exists', category="error")
        elif req.status_code == 503:
            flash('Something went wrong!', category="error")
        else:
            session["name"] = userData["name"]
            session["user_id"] = userData["user_id"]
            return redirect(url_for('views.getrecipes'))

    return render_template("signup.html")

