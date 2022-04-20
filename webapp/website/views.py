from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")




'''
Rendering html pages - 

put home page template code inside home.html

def home():
    return render_template("home.html")
'''