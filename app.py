from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from transformers import pipeline
import os

app = Flask(__name__)

# Allow CORS for both local and GitHub Pages
CORS(app, origins=["http://127.0.0.1:5000", "http://localhost:5000", "https://lubnam.github.io"])

# Load the Hugging Face model
classifier = pipeline("text-classification", model="Lubna1/diagnoser_v1", tokenizer="Lubna1/diagnoser_v1")

@app.route("/")
def home():
    # Serve the index.html page when the root route is accessed
    return render_template("index.html")  # Make sure index.html is inside a 'templates' folder

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    input_text = data.get("text", "")

    try:
        result = classifier(input_text)[0]
        print(result)
        label = result['label']
        score = result['score']
        # Adjust diagnosis based on label (ensure this matches your model's labels)
        diagnosis = 'Appendicitis' if label == 'LABEL_0' else 'Other Abdominal Disease'

        return jsonify({
            "diagnosis": diagnosis,
            "confidence": round((score * 100)-4, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
