from flask import Blueprint, render_template, redirect

home_views = Blueprint('home', __name__)

@home_views.route('/')
def login():
    return render_template('pages/login.html')