"""
This file handles all REST API calling and receiving of cars
"""
from flask import Blueprint

from flask import flash, render_template, request, redirect, url_for
import requests
from auxilaryapi import get_image_link
from routes.authenticate import header, get_login_status, login_required

#API_BASE_URL = 'http://195.148.21.89:5000/api/'
API_BASE_URL = 'http://127.0.0.1:5000/api/'
car_bp = Blueprint('car', __name__)

page_data = {'login_status': None}


@car_bp.route('/')
def home():
    """
    Gets cars information from API endpoint and renders it on home.html

    Returns:
        Rendered HTML page for cars information
    Raises:
        ConnectionError: If connection fails with endpoint API
        TimeOutError : If request takes longer then 20 seconds
    Usages:
        call this function from route in Flask web application to display cars information
    """
    page_data['login_status'] = get_login_status()
    response = requests.get(f'{API_BASE_URL}cars/')
    cars = response.json()
    # don't show cars that are returned
    cars = [car for car in cars if car['status'] != 'returned']
    status = request.args.get('status', 'all')
    if status == 'rented':
        print("Getting Rented Cars")
        cars = [car for car in cars if car['status'] == 'rented']
    elif status == 'available':
        print("Getting Available Cars")
        cars = [car for car in cars if car['status'] == 'available']
    else:
        print("Showing all cars")

    return render_template('home.html', cars=cars, login_status=get_login_status, page_data=page_data)


@car_bp.route('/car/<int:car_id>')
def car_details(car_id):
    """
    Gets car detail information from API endpoint and renders it on car_details.html

    Args:
        car_id: id of car record which needs to be displayed
    Returns:
        Rendered HTML page for car detail information
    Raises:
        ConnectionError: If connection fails with endpoint API
        TimeOutError : If request takes longer then 20 seconds
    Usages:
        call this function from route in Flask web application to display car details of one record
    """
    page_data['login_status'] = get_login_status()
    response = requests.get(f'{API_BASE_URL}car/{car_id}', timeout=20)
    car_data = response.json()
    car = car_data[0] if car_data else {}

    keys = list(car.keys())
    keys.remove('id')
    keys.remove('links')
    print(f"Car name is {car['name']}")
    # image_link = get_image_link(car)
    image_link = "https://i.ytimg.com/vi/cDGM76Ig9zM/maxresdefault.jpg"
    return render_template('car_details.html', car=car, keys=keys, image_link=image_link, page_data=page_data)


@car_bp.route('/car/<int:car_id>/delete', methods=['POST'])
@login_required
def delete_car(car_id):
    """
     Deletes car record from API endpoint and navigates to home.html to render cars records on home.html

     Args:
         car_id: id of car record which needs to be deleted
     Returns:
         Rendered HTML page for car detail information
         Error : if the deletes operation not performed
     Raises:
         ConnectionError: If connection fails with endpoint API
         TimeOutError : If request takes longer then 20 seconds
     Usages:
         call this function from route in Flask web application to delete car information
     """
    response = requests.delete(f'{API_BASE_URL}car/{car_id}', headers=header)
    if response.status_code == 204:
        return redirect(url_for('car.home'))
    else:
        return f'Error: {response.status_code}', response.status_code


@car_bp.route('/car/<int:car_id>/edit', methods=['GET', 'POST', 'PUT'])
@login_required
def edit_car(car_id):
    """
     Edits car  information from API endpoint and renders it on edit_car.html

     Args:
         car_id: id of car record which needs to be updated
     Returns:
         Rendered HTML page for car detail information if  error occurs
         Rendered HTML page of car information if successfull
     Raises:
         ConnectionError: If connection fails with endpoint API
         TimeOutError : If request takes longer then 20 seconds
     Usages:
         call this function from route in Flask web application to display and edit car information
     """
    page_data['login_status'] = get_login_status()
    # Get the existing car from the API
    car = requests.get(f'{API_BASE_URL}car/{car_id}/').json()[0]

    if request.method == 'POST':

        car = {}
        user_inputs = ''
        # looping through form to make it dynamic
        try:
            for key, user_inputs in request.form.items():
                if key == 'rent_price':
                    car[key] = float(user_inputs)
                if key == 'year':
                    car[key] = int(user_inputs)
                else:
                    car[key] = user_inputs
        except ValueError:
            flash(f'Enter Valid Numbers `{user_inputs}`', 'danger')
            return redirect(url_for('car.edit_car', car_id=car_id))
        # Send a PUT request to update the car in the API
        response = requests.put(f'{API_BASE_URL}car/{car_id}/', json=car, timeout=20, headers=header)
        if response.status_code == 204:
            print("Car updated successfully")
            # if the edit is successful go to the car details page
            return redirect(url_for('car.car_details', car_id=car_id))
        else:
            # Error updating car
            flash(f'Error updating car. {response.status_code}', 'danger')
            return redirect(url_for('car.edit_car', car_id=car_id, page_data=page_data))

    else:
        print("Rendering Edit form for cars")
        return render_template('edit_car.html', car=car, page_data=page_data)


@car_bp.route('/car/add', methods=['POST', 'GET'])
@login_required
def add_car():
    """
     Adds car  information from API endpoint and renders it on add_car.html

     Returns:
         Rendered HTML page for car detail information if  error occurs
         Rendered HTML page of cars information if successfull
     Raises:
         ConnectionError: If connection fails with endpoint API
         TimeOutError : If request takes longer then 20 seconds
     Usages:
         call this function from route in Flask web application to add car information
     """
    page_data['login_status'] = get_login_status()
    if request.method == 'POST':

        car = {}
        user_inputs = ''
        # looping through form to make it dynamic
        try:
            for key, user_inputs in request.form.items():
                if key == 'rent_price':
                    car[key] = float(user_inputs)
                if key == 'year':
                    car[key] = int(user_inputs)
                else:
                    car[key] = user_inputs
        except ValueError:
            flash(f'Enter Valid Numbers `{user_inputs}`', 'danger')
            return redirect(url_for('car.add_car'))
        # Send a PUT request to update the car in the API
        response = requests.post(f'{API_BASE_URL}cars/', json=car, timeout=20, headers=header)
        if response.status_code == 201:
            print("Car added successfully")
            # if the edit is successful go to the car details page
            return redirect(url_for('car.home'))
        else:
            # Error updating car
            flash(f'Error adding car. {response.status_code}', 'danger')
            return redirect(url_for('car.add_car'))

    else:
        # Get the existing car from the API for keys to make form dynamic
        car = requests.get(f'{API_BASE_URL}car/{2}/', timeout=20).json()[0]
        print("Rendering Add form for cars")
        return render_template('add_car.html', car=car, page_data=page_data)
