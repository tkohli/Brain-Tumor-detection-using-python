from sqlite3.dbapi2 import Connection
from flask import Blueprint, render_template, request, flash, jsonify,session
from flask_login import login_manager, login_required, current_user
from sqlalchemy.sql.functions import user
from . import db
from . import models
import json
from .models import User, get_user
import os
from flask import Flask, render_template, request
from predictor import check
import sqlite3 as sql

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
views = Blueprint('views', __name__)
views._static_folder = ''

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html')

@views.route('/list' ,methods=['GET', 'POST'])
def list():
    con = sql.connect("Outputdb.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    return render_template("list.html",rows = data)


@views.route('/search', methods=['GET', 'POST'])
def search():
    with sql.connect("Outputdb.db") as con:
        cur = con.cursor()
        email = request.form['email']
        email = str(email)
        print(email)
        query = "SELECT * FROM students WHERE username="+"\'"+email+"\'"
        c = con.execute(query)
        # c = con.execute('''SELECT * FROM students WHERE username= ?'''.format(email))
        data = c.fetchall()
        con.commit()
        return render_template("list.html",rows = data)

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    return render_template('upload.html')


@views.route('/uploaded', methods=['GET', 'POST'])
def uploaded():
    target = os.path.join(APP_ROOT, '')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist('file'):
        print(file)
        filename = file.filename
        print(filename)
        dest = '/'.join([target, filename])
        print(dest)
        file.save(dest)
    
    st = (str(current_user))
    for s in st:
        if s.isdigit():
            print(s)
            uid = s
    user = User.query.filter_by(id=uid).first()
    print(user.email)
    status = check(filename)
    nm = user.email
    location = dest
    details = request.form['details']
    print(status,"Value")
    # pin = request.form[Rating]
    if status == True:
        val = 'Brain Tumor detected!!!'
    else:
        val = "No brain tumor"
    with sql.connect("Outputdb.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO students (username,image,BrainTumor,details) VALUES (?,?,?,?)",[str(nm),location,val,details] ) 
        con.commit()
        msg = "Record successfully added"
        
        

        
    return render_template('complete.html', image_name=filename, predvalue=status)

if __name__ == "main":
    app.run(port=4555, debug=True)

    