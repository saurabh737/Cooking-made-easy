from distutils.log import error
from flask import Blueprint, render_template, request, flash, redirect, url_for
import requests, json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
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
        
        if req.status_code == 200:
            return render_template("getrecipes.html")
        elif req.status_code == 401:
            flash('Incorrect credentials!', category="error")

    return render_template("login.html")

@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))

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
            #flash('Account created!', category='success')
            return render_template("getrecipes.html")

    return render_template("signup.html")