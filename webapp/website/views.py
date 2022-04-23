from flask import Blueprint, render_template
from flask_login import current_user
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/getrecipes')
def getrecipes():
    return render_template("getrecipes.html")
