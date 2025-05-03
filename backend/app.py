from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

app = Flask(__name__)
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_URL = "https://api-inference.huggingface.co/models/Lubna1/diagnoser_v1"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        response = requests.post(
            MODEL_URL,
            headers={
                "Authorization": f"Bearer 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",
                "Content-Type": "application/json",
                "Wait-For-Model": "true"
            },
            json=request.json,
            timeout=30  # Wait up to 30 seconds for model to load
        )
        response.raise_for_status()  # Raise HTTP errors
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
