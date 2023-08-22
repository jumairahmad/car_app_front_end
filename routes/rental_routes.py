"""
This file handles all REST API calling and receiving of Rentals
"""
from flask import Blueprint

from flask import Flask, flash, render_template, request, redirect, url_for
import requests
from routes.authenticate import header, get_login_status, login_required

#API_BASE_URL = 'http://195.148.21.89:5000/api/'
API_BASE_URL = 'http://127.0.0.1:5000/api/'


rental_bp = Blueprint('rental', __name__)
page_data = {'login_status': None}


@rental_bp.route('/rentals/')
def rental_home():
    """
    Gets rental information for API endpoint and renders it on rentals.html

    Returns:
        Rendered HTML page for rental information
    Raises:
        ConnectionError: If connection fails with endpoint API
        TimeOutError : If request takes longer then 20 seconds
    Usages:
        call this function from route in Flask web application to display rental information
    """
    print("Getting rental page")
    page_data['login_status'] = get_login_status()
    response = requests.get(f'{API_BASE_URL}rentals/', timeout=20)
    customers = response.json()
    return render_template('rentals.html', rentals=customers, page_data=page_data)


@rental_bp.route('/rental/<int:rental_id>')
@login_required
def rental_details(rental_id):
    """
    Gets rental detail information from API endpoint and renders it on rental_details.html

    Args:
        rental_id: id of rental record which needs to be displayed
    Returns:
        Rendered HTML page for rental detail information
    Raises:
        ConnectionError: If connection fails with endpoint API
        TimeOutError : If request takes longer then 20 seconds
    Usages:
        call this function from route in Flask web application to display rental details of one record
    """
    page_data['login_status'] = get_login_status()
    response = requests.get(f'{API_BASE_URL}rental/{rental_id}', timeout=20, headers=header)
    ren_data = response.json()
    print(f"Showing rental details {ren_data}")
    rental = ren_data[0] if ren_data else {}

    keys = list(rental.keys())
    keys.remove('id')
    keys.remove('links')
    print(rental)

    return render_template('rental_details.html', rental=rental, keys=keys, page_data=page_data)


@rental_bp.route('/rental/<int:rental_id>/delete', methods=['POST'])
@login_required
def delete_rental(rental_id):
    """
     Deletes rental record from API endpoint and navigates to rental_home to render rentals records on rental.html

     Args:
         rental_id: id of rental record which needs to be deleted
     Returns:
         Rendered HTML page for rental detail information
         Error : if the deletes operation not performed
     Raises:
         ConnectionError: If connection fails with endpoint API
         TimeOutError : If request takes longer then 20 seconds
     Usages:
         call this function from route in Flask web application to delete rental information
     """
    response = requests.delete(f'{API_BASE_URL}rental/{rental_id}', headers=header)
    if response.status_code == 204:
        return redirect(url_for('rental.rental_home'))
    else:
        return f'Error: {response.status_code}', response.status_code


@rental_bp.route('/rental/<int:rental_id>/edit', methods=['GET', 'POST', 'PUT'])
@login_required
def edit_rental(rental_id):
    """
     Edits rental  information from API endpoint and renders it on edit_rental.html

     Args:
         rental_id: id of rental record which needs to be updated
     Returns:
         Rendered HTML page for rental detail information if  error occurs
         Rendered HTML page of rentals information if successfull
     Raises:
         ConnectionError: If connection fails with endpoint API
         TimeOutError : If request takes longer then 20 seconds
     Usages:
         call this function from route in Flask web application to display and edit rental information
     """
    # Get the existing rental from the API
    page_data['login_status'] = get_login_status()
    rental = requests.get(f'{API_BASE_URL}rental/{rental_id}/', timeout=20, headers=header).json()[0]

    if request.method == 'POST':

        rental = {}
        # looping through form to make it dynamic
        for key, value in request.form.items():
            if key == 'car_id':
                rental[key] = int(value)
            if key == 'customer_id':
                rental[key] = int(value)
            else:
                rental[key] = value

        # Send a PUT request to update the rental in the API
        response = requests.put(f'{API_BASE_URL}rental/{rental_id}/', json=rental, timeout=20, headers=header)
        print("after edited", rental)
        if response.status_code == 204:
            # Rental updated successfully
            flash('Rental updated successfully!', 'success')
            return redirect(url_for('rental.rental_details', rental_id=rental_id))
        else:
            # Error updating rental
            flash('Error updating rental. Please try again.', 'danger')
            return redirect(url_for('rental.edit_rental', rental_id=rental_id))

    else:
        # Render the edit rental form
        return render_template('edit_rental.html', rental=rental, page_data=page_data)


@rental_bp.route('/rental/<int:car_id>/add', methods=['GET', 'POST', 'PUT'])
@login_required
def add_rental(car_id):
    """
     Adds rental  information from API endpoint and renders it on add_rental.html

     Args:
         car_id: id of car record which needs to be rented for customer
     Returns:
         Rendered HTML page for rental detail information if  error occurs
         Rendered HTML page of rentals information if successfull
     Raises:
         ConnectionError: If connection fails with endpoint API
         TimeOutError : If request takes longer then 20 seconds
     Usages:
         call this function from route in Flask web application to add rental information
     """

    # lets get customers from our data base so that we can pop up customer name to select customer
    page_data['login_status'] = get_login_status()
    response = requests.get(f'{API_BASE_URL}customers/', timeout=20)
    customers = response.json()

    # Get the existing rental record from the API to dynamically create a form
    rental = requests.get(f'{API_BASE_URL}rental/{4}/', timeout=20, headers=header).json()[0]
    if request.method == 'POST':

        rental = {'car_id': int(car_id)}
        # looping through form to make it dynamic
        for key, value in request.form.items():

            if key == 'customerNames':

                for customer in customers:
                    if customer['name'].lower() == value.lower():
                        rental['customer_id'] = int(customer['id'])
            else:
                rental[key] = value

        print("before adding", rental)
        # Send a PUT request to update the car in the API
        response = requests.post(f'{API_BASE_URL}rentals/', json=rental, timeout=20, headers=header)
        print("after adding", rental)
        if response.status_code == 201:
            # Rental inserted successfully
            flash('Rental Inserted successfully!', 'success')
            return redirect(url_for('rental.rental_home'))
        else:
            # Error updating car
            flash('Error updating rental. Please try again.', 'danger')
            return redirect(url_for('rental.add_rental', car_id=car_id, rental=rental, customers=customers))

    else:
        # Render the add rental form
        return render_template('add_rental.html', car_id=car_id, rental=rental, customers=customers,
                               page_data=page_data)
