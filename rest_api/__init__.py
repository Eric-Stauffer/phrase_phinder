from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

from rest_api import routes

