from flask import Flask
from flask.ext.cors import CORS

app = Flask(__name__, static_url_path='')
CORS(app)

from app import views
