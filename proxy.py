from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    response = requests.post(
        "https://api-inference.huggingface.co/models/Lubna1/diagnoser_v1",
        headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"},
        json=request.json
    )
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(port=5000)
