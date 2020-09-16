from flask import Flask

app = Flask(__name__)

from rest_api import routes
