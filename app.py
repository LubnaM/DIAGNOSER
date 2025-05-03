#This endpoint (app.py, acting as Flask server) will respond to POST /predict with a JSON #diagnosis.

from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load the model once when the app starts
classifier = pipeline("text-classification", model="Lubna1/diagnoser_v1", tokenizer="Lubna1/diagnoser_v1")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    input_text = data.get("text", "")

    try:
        result = classifier(input_text)[0]
        label = result['label']  # e.g., LABEL_1 or LABEL_0
        score = result['score']

        # Map label to diagnosis
        diagnosis = "Appendicitis" if label == "LABEL_1" else "Other Abdominal Disease"

        return jsonify({
            "diagnosis": diagnosis,
            "confidence": round(score * 100, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
