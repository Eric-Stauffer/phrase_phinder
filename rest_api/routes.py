from flask import request, jsonify
from rest_api import app
from rest_api import Search

@app.route('/',methods=['POST'])
@app.route('/search', methods=['POST'])
def search():
    search_input = request.json
    response = Search.main(search_input["phrase"])
    return response