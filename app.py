from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)  # ✅ Allows CORS from anywhere (for testing/deployment)

classifier = pipeline("text-classification", model="Lubna1/diagnoser_v1", tokenizer="Lubna1/diagnoser_v1")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    input_text = data.get("text", "")

    try:
        result = classifier(input_text)[0]
        label = result['label']
        score = result['score']

        diagnosis = "Appendicitis" if label == "LABEL_1" else "Other Abdominal Disease"

        return jsonify({
            "diagnosis": diagnosis,
            "confidence": round(score * 100, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT or default to 5000
    app.run(host="0.0.0.0", port=port)
