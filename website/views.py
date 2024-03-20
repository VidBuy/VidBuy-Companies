
# views.py

from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
import random
from flask_login import login_required, current_user
from sqlalchemy.sql import func  # Import the 'func' module
import json
from .models import User
from werkzeug.security import generate_password_hash
from . import db

from datetime import datetime
import datetime as dt

# from .DateToolKit

current_date = dt.date.today()
formatted_date = current_date.strftime("%Y-%m-%d")
current_year = current_date.strftime("%Y")
current_time = datetime.now().strftime("%H:%M")

from .VertexClient import dbORM
from .DateToolKit import clean_date
from . import encrypt_k7s2

import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

def oppositeTheme(theme):
  if theme == 'light':
    return 'dark'
  else:
    return 'light'

def go_to(screen_id):
  
  User = dbORM.get_all("USER")
  # company = dbORM.get_all("Company")

  def remove_duplicates(original_list):
    duplicates_removed_list = []
    [duplicates_removed_list.append(x) for x in original_list if x not in duplicates_removed_list]
    return duplicates_removed_list

  if dbORM == None:
  	def radFun(x_range):
  		return random.choice(x_range)

  	num1, num2, num3, num4, num5, num6 = radFun(range(10)), radFun(range(10)), radFun(range(10)), radFun(range(10)), radFun(range(10)), radFun(range(10))
  	return render_template("page-error.html", eid=f"00x{num1}{num2}{num3}{num4}-{num5}{num6}", ecd="EC-002")
  
  return render_template("UDP.html",
    ScreenID = screen_id,
    CurrentUser = User[f'{current_user.id}'],
    CurrentDate=clean_date(formatted_date),
    AppTheme=User[f'{current_user.id}']['app_theme']
    )


@views.route('/')
def index():
	if dbORM == None:
	  	def radFun(x_range):
	  		return random.choice(x_range)

	  	num1, num2, num3, num4, num5, num6 = radFun(range(10)), radFun(range(10)), radFun(range(10)), radFun(range(10)), radFun(range(10)), radFun(range(10))
	  	return render_template("page-error.html", eid=f"00x{num1}{num2}{num3}{num4}-{num5}{num6}", ecd="EC-002")

	return render_template("INDEX.html")


@views.route('/dashboard')
def viewDashBoard():
  
  return go_to(screen_id=1)

@views.route('/dashboard/<string:screen_id>')
def goToScreen(screen_id):

  return go_to(screen_id=screen_id)

@views.route('/edit-profile', methods=['POST'])
def editProfile():
  
  if request.form['user_password'] == "":
    

    _ = {
      "name": request.form['user_name'],
      "email": request.form['user_email'],
      "gender": request.form['user_gender']
    }
  else:
    _ = {
      "name": request.form['user_name'],
      "email": request.form['user_email'],
      "gender": request.form['user_gender'],
      "password": generate_password_hash(request.form['user_password'])
    }

  dbORM.update_entry("USER", f"{dbORM.find_one('USER', 'id', str(current_user.id))}", _)
  

  return go_to(screen_id=str(request.form['screen_id']))

@views.route('/add-to-company', methods=['POST'])
def addTocompany():
  
  data_pack = json.loads(request.data)

  _ = {
    'name':  data_pack['name'],
    'amount':  data_pack['amount'],
    '_for':  data_pack['_for'],
    'where':  data_pack['where'],
    'description':  data_pack['description'],
    'timestamp': f'{current_time}',
    'datestamp': f'{current_date}'
  }

  dbORM.add_entry("company", f"{encrypt_k7s2.encrypter(str(_))}")

  return go_to(screen_id=data_pack['screen'])

@views.route('/change-app-theme', methods=['POST'])
def changeAppTheme():
  data = json.loads(request.data)

  

  dbORM.update_entry("USER", f"{dbORM.find_one('USER', 'id', str(current_user.id))}", {"app_theme": f"{oppositeTheme(data['current_app_theme'])}"})
    

  return jsonify({})