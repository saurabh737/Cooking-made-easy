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
    cooking_time = request.form.get("cooking_time")
    
    #print(n_ingredients, cooking_time)
    if n_ingredients or cooking_time:
        url = 'http://127.0.0.1:3000/recipes/filter?user_id='+ str(session["user_id"])

        if n_ingredients and not cooking_time:
            url += '&n_steps=' + str(n_ingredients)
        elif cooking_time and not n_ingredients:
            url += '&cooktime=' + str(cooking_time)
        elif n_ingredients and cooking_time:
            url += '&cooktime=' + str(cooking_time) + '&n_steps=' + str(n_ingredients)
        
        req = requests.get(url)
        filter_data = req.json()
        return render_template("getrecipes.html", req_data = filter_data)

    else:

        status_show = request.args.get('status', None)
        recipe_id_show = request.args.get('recipe_id_get', None)

        if len(session) != 0:
            data = {}
            data['user_id'] = session['user_id']
            data['recipe_id'] = recipe_id_show

            if status_show is not None:

                if status_show == 'True':
                    url = 'http://127.0.0.1:3000/activity/deletefavourite'
                    req_status = requests.post(url, json = data)
                else:
                    url = 'http://127.0.0.1:3000/activity/addfavourite'
                    req_status = requests.post(url, json = data)

            url = 'http://127.0.0.1:3000/recipes/getall?user_id='+ str(session["user_id"])
            print(url)
            req = requests.get(url)
            req_data = req.json()
            
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


@views.route('/userfavourites', methods = ['GET','POST'])
def userfavourites():

    if len(session) != 0:
        
        recipe_id_show = request.args.get('recipe_id_get', None)
        status_show = request.args.get('status', None)
        
        data = {}
        data['user_id'] = session['user_id']
        data['recipe_id'] = recipe_id_show

        if status_show:
            url_status = 'http://127.0.0.1:3000/activity/deletefavourite'
            req_status = requests.post(url_status, json = data)

        url = 'http://127.0.0.1:3000/activity/getfavourite'
        req = requests.post(url, json = data)
        # user_data = req.json()
        print(req.status_code, url)

        if req.status_code == 204:
            user_data = []
        else:
            user_data = req.json()
            print(user_data)

        return render_template("userfavourites.html", req_data = user_data)
    else:
        return render_template("userfavourites.html")