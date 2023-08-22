import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_car_details_invalid_id(client):
    response = client.get('/car/invalid_id')
    assert response.status_code == 404


def test_delete_car(client):
    response = client.post('/car/21/delete')
    assert response.status_code == 302


def test_delete_car_invalid_id(client):
    response = client.post('/car/invalid_id/delete')
    assert response.status_code == 404


def test_edit_car_invalid_id(client):
    response = client.get('/car/invalid_id/edit')
    assert response.status_code == 404


def test_customers_page(client):
    response = client.get('/customers/')
    assert response.status_code == 200


def test_customer_details_invalid_id(client):
    response = client.get('/customer/invalid_id')
    assert response.status_code == 404


def test_delete_customer(client):
    response = client.post('/customer/21/delete')
    assert response.status_code == 302


def test_delete_customer_invalid_id(client):
    response = client.post('/customer/invalid_id/delete')
    assert response.status_code == 404


def test_edit_customer_invalid_id(client):
    response = client.get('/customer/invalid_id/edit')
    assert response.status_code == 404


def test_rentals_page(client):
    response = client.get('/rentals/')
    assert response.status_code == 200


def test_rentals_details_invalid_id(client):
    response = client.get('/rental/invalid_id')
    assert response.status_code == 404


def test_delete_rental(client):
    response = client.post('/rental/21/delete')
    assert response.status_code == 302


def test_delete_rental_invalid_id(client):
    response = client.post('/rental/invalid_id/delete')
    assert response.status_code == 404


def test_edit_rental_invalid_id(client):
    response = client.get('/rental/invalid_id/edit')
    assert response.status_code == 404
