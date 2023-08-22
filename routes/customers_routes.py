"""
This file handles all REST API calling and receiving of Customers
"""
from flask import Blueprint

from flask import Flask, flash, render_template, request, redirect, url_for
import requests
from routes.authenticate import header, get_login_status, login_required

#API_BASE_URL = 'http://195.148.21.89:5000/api/'
API_BASE_URL = 'http://127.0.0.1:5000/api/'


customer_bp = Blueprint('customer', __name__)

page_data = {'login_status': None}

@customer_bp.route('/customers/')
def customer_home():
    """
       Gets customers information for API endpoint and renders it on customers.html

       Returns:
           Rendered HTML page for customers information
       Raises:
           ConnectionError: If connection fails with endpoint API
           TimeOutError : If request takes longer then 20 seconds
       Usages:
           call this function from route in Flask web application to display Customers information
       """
    print("Getting customers page")
    page_data['login_status'] = get_login_status()
    response = requests.get(f'{API_BASE_URL}customers/', timeout=20)
    customers = response.json()
    return render_template('customers.html', customers=customers, page_data=page_data)


@customer_bp.route('/customer/<int:customer_id>')
def customer_details(customer_id):
    """
     Gets customer detail information from API endpoint and renders it on customer_details.html

     Args:
         customer_id: id of customer record which needs to be displayed
     Returns:
         Rendered HTML page for customer detail information
     Raises:
         ConnectionError: If connection fails with endpoint API
         TimeOutError : If request takes longer then 20 seconds
     Usages:
         call this function from route in Flask web application to display customer details of one record
     """
    page_data['login_status'] = get_login_status()
    response = requests.get(f'{API_BASE_URL}customer/{customer_id}', timeout=20)
    cust_data = response.json()
    customer = cust_data[0] if cust_data else {}

    keys = list(customer.keys())
    keys.remove('id')
    keys.remove('links')

    return render_template('customer_details.html', cus=customer, keys=keys, page_data=page_data)


@customer_bp.route('/customer/<int:customer_id>/delete', methods=['POST'])
@login_required
def delete_customer(customer_id):
    """
      Deletes customer record from API endpoint and navigates to customer.html to render customers records

      Args:
          customer_id: id of customer record which needs to be deleted
      Returns:
          Rendered HTML page for customer detail information
          Error : if the deletes operation not performed
      Raises:
          ConnectionError: If connection fails with endpoint API
          TimeOutError : If request takes longer then 20 seconds
      Usages:
          call this function from route in Flask web application to delete customer information
      """
    response = requests.delete(f'{API_BASE_URL}customer/{customer_id}', headers=header)
    if response.status_code == 204:
        return redirect(url_for('customer.customer_home'))
    else:
        return f'Error: {response.status_code}', response.status_code


@customer_bp.route('/customer/<int:customer_id>/edit', methods=['GET', 'POST', 'PUT'])
@login_required
def edit_customer(customer_id):
    """
     Edits customer  information from API endpoint and renders it on edit_customer.html

     Args:
         customer_id: id of customer record which needs to be updated
     Returns:
         Rendered HTML page for customer detail information if  error occurs
         Rendered HTML page of customers information if successfull
     Raises:
         ConnectionError: If connection fails with endpoint API
         TimeOutError : If request takes longer then 20 seconds
     Usages:
         call this function from route in Flask web application to display and edit customer information
     """
    # Get the existing customer from the API
    page_data['login_status'] = get_login_status()
    customer = requests.get(f'{API_BASE_URL}customer/{customer_id}/', timeout=20).json()[0]

    if request.method == 'POST':

        customer = {}
        # looping through form to make it dynamic
        for key, value in request.form.items():
            customer[key] = value

        # Send a PUT request to update the customer in the API
        response = requests.put(f'{API_BASE_URL}customer/{customer_id}/', json=customer, timeout=20, headers=header)
        print("after edited", customer)
        if response.status_code == 204:
            # Customer updated successfully
            flash('Customer updated successfully!', 'success')
            return redirect(url_for('customer.customer_details', customer_id=customer_id))
        else:
            # Error updating customer
            flash('Error updating customer. Please try again.', 'danger')
            return redirect(url_for('customer.edit_customer', customer_id=customer_id))

    else:
        # Render the edit customer form
        return render_template('edit_customer.html', customer=customer, page_data=page_data)


@customer_bp.route('/customer/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    """
     Adds customer information to API endpoint and renders it on add_customer.html

     Returns:
         Rendered HTML page for customer detail information if  error occurs
         Rendered HTML page of customer information if successfull
     Raises:
         ConnectionError: If connection fails with endpoint API
         TimeOutError : If request takes longer then 20 seconds
     Usages:
         call this function from route in Flask web application to add customer information
     """
    if request.method == 'POST':

        customer = {}
        # looping through form to make it dynamic
        for key, value in request.form.items():
            if key == 'car_id':
                customer[key] = int(value)
            else:
                customer[key] = value
        # Send a POST request to insert the customer in the API
        response = requests.post(f'{API_BASE_URL}customers/', json=customer, timeout=20, headers=header)
        if response.status_code == 201:
            flash('Customer Inserted successfully!', 'success')
            return redirect(url_for('customer.customer_home'))
        else:
            # Error inserting customer
            flash('Error Inserting customer. Please try again.', 'danger')
            return redirect(url_for('customer.add_customer'))

    else:
        # Get the existing customer from the API to dynamically render form
        customer = requests.get(f'{API_BASE_URL}customer/{3}/', timeout=20).json()[0]
        return render_template('add_customer.html', customer=customer, page_data=page_data)
