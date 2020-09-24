
# # A very simple Flask Hello World app for you to get started with...

# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello from Flask!'

from flask import Flask, request, render_template
from flask_cors import CORS
import Search

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))

app = CustomFlask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search():
    search_input = request.json
    response = Search.main(search_input["phrase"])
    return response

@app.route('/')
def home():
    return render_template("index.html")