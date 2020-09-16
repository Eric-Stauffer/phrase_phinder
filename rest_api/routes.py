from flask import request, jsonify
from flaskr import app
from flaskr import Search


@app.route('/search', methods=['POST'])
def search():
    search_input = request.json

    response = Search.main(search_input["phrase"])

    return response