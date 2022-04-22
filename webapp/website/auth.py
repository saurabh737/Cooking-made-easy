from flask import Blueprint, render_template, request, flash
import requests, json

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template("login.html", boolean = True)

@auth.route('/logout')
def logout():
    return "<p> Logout </p>"

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    email = request.form.get('email')
    firstName = request.form.get('firstName')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if password1 != password2:
        flash('Passwords dont match', category="error")

    data = {}

    data['email'] = email
    data['password'] = password1
    data['name'] = firstName
    
    if request.method == 'POST':
        req = requests.post('http://127.0.0.1:3000/user/signup', json = data)
    
        if req.status_code == 401:
            flash('Email already exists', category="error")
        elif req.status_code == 503:
            flash('Something went wrong!', category="error")
        else:
            flash('Account created!', category='success')
            return render_template("base.html")

    return render_template("signup.html")