from flask import Flask, jsonify, request
import json
import os
from models import probe_model_5l_profit
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
@app.route('/')
def hello():
    return 'Hello'

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the file part is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    # If no file was selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Process the file (ensure it's JSON)
    try:
        data = json.load(file)
        result = probe_model_5l_profit(data["data"])
        return jsonify(result), 200
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format'}), 400

if __name__ == '__main__':
    app.run(debug=True)
