from urllib.request import urlopen
from flask import Blueprint, render_template, jsonify
from flask_login import current_user
from flask_login import login_required, current_user
# from requests import session
import requests
import json
from flask import Blueprint, render_template, request, flash, redirect, url_for, session

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/getrecipes', methods = ['GET','POST'])
def getrecipes():
    
    #print(session['name'])
    n_ingredients = request.form.get("n_ingredients")
    input_ingredients = request.form.get("input_ingredients")
    cooking_time = request.form.get("cooking_time")

    if len(session) != 0:
        url = 'http://127.0.0.1:3000/recipes/getall?user_id='+ str(session["user_id"])
        print(url)
        req = requests.get(url)
        req_data = req.json()
        #print(req_data)
    
        return render_template("getrecipes.html", req_data = req_data)

    else:
        return render_template("getrecipes.html")
        
@views.route('/recipeinfo', methods = ['GET','POST'])
def recipeinfo():
    recipe_id_show = request.args.get('recipe_id_get', None)
    
    if len(session) != 0:
        url = 'http://127.0.0.1:3000/recipes/metadata?recipe_id='+ str(recipe_id_show) + '&user_id=' + str(session["user_id"])
        req = requests.get(url)
        recipe_data = req.json()
        print(recipe_data)

    
    return render_template("recipeinfo.html", recipe_data = recipe_data)

