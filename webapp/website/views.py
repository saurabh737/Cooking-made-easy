from flask import Blueprint, render_template
from flask_login import current_user
from flask_login import login_required, current_user
# from requests import session
from flask import Blueprint, render_template, request, flash, redirect, url_for, session

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/getrecipes')
def getrecipes():
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=In hereeeeeeeeee')
    print(session['name'])
    return render_template("getrecipes.html")
