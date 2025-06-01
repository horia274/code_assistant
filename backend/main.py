from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from code_analyzer import analyze

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Hello!"})

@app.route('/analyze-code', methods=['POST'])
def analyze_code():
    data = request.json
    analysis = analyze(data)
    return jsonify(analysis)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
