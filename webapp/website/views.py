from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/getrecipes')
def getrecipes():
    return render_template("getrecipes.html")
