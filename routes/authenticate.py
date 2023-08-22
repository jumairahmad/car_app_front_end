"""This file handles authentication tokens if a user wants to login inorder to change something"""

from flask import Blueprint,flash
from flask import render_template, request, redirect, url_for, session
import json
from functools import wraps
import requests

API_BASE_URL = 'http://127.0.0.1:5000/api/'
auth_bp = Blueprint('login', __name__)

header = {'token': None}

LOGIN_STATUS = True
original_url = None

page_data = {'login_status': None}

@auth_bp.route('/login/', methods=['GET', 'POST'])
def home():
    global LOGIN_STATUS
    global original_url
    original_url = None
    if LOGIN_STATUS is True:
        print("You are already logged in ")
        return redirect(url_for('car.home'))
    elif request.method == 'GET':
        session['original_url'] = request.referrer
        return render_template('login.html', page_data=page_data)
    elif request.method == 'POST':
        try:
            print("Getting token for the user")
            # Code to execute when the method is POST
            username = request.form['username']
            password = request.form['password']
            payload = {'password': password, 'username': username}
            # Generate JWT token
            response = requests.post(f'{API_BASE_URL}/login', data=payload)
            token = json.loads(response.text)['token']
            header['token'] = token
            LOGIN_STATUS = True
            print(header)
            print(f"Your Login Status is now {LOGIN_STATUS}")
            original_url = session.pop('original_url', None)  # Get the original request URL from the session
            if original_url:
                return redirect(original_url)
            else:
                return redirect(url_for('car.home'))
        except Exception as e:
            print(e)
            flash('Invalid User Name or Password', 'danger')
            return redirect(url_for('login.home'))

def get_login_status():
    print(f"Giving latest login status that is {LOGIN_STATUS}")
    return LOGIN_STATUS


def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        login_status = get_login_status()
        if login_status is not True:
            print("You are need to logged in")
            return redirect(url_for('login.home'))
        else:
            return route_function(*args, **kwargs)

    return wrapper
