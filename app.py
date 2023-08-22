"""
This file is starting point for our application
"""

from pathlib import Path

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

sys.path.append(str(Path(__file__).resolve().parent))
from routes.cars_routes import car_bp
from routes.customers_routes import customer_bp
from routes.rental_routes import rental_bp
from routes.authenticate import auth_bp

from mycarapp import app

app.register_blueprint(car_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(rental_bp)
app.register_blueprint(auth_bp)


@app.context_processor
def inject_page_data():
    pdata = {
        'title': 'Cars',
        'description': 'Welcome to my cars!',
        'username': None
    }
    return dict(pdata=pdata)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
