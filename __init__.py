import secrets
from flask import Flask
from flask_caching import Cache

API_BASE_URL = 'http://195.148.21.89:5000/api/'
SECRET_KEY = secrets.token_hex(10)


# API_BASE_URL = 'http://127.0.0.1:5000/api/'
def create_app():
    app = Flask(__name__)

    app.config["CACHE_TYPE"] = "FileSystemCache"
    app.config["CACHE_DIR"] = "cache"
    app.config['SECRET_KEY'] = SECRET_KEY
    return app


app = create_app()
cache = Cache(app)
header = {'token':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiMTIzNCIsImV4cGlyYXRpb24iOjE2ODI2MzMzMjV9.W7Af9ap64pVDxe93f_wfL8Hrp62L42BgdZh3tpcY0A8'}

