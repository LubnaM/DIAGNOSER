async function diagnose() {
  const text = document.getElementById("symptoms").value;
  const resultDiv = document.getElementById("result");
  
  if (!text) {
    resultDiv.innerHTML = "Please describe symptoms";
    return;
  }

  resultDiv.innerHTML = "Analyzing...";

  try {
    const response = await fetch(
      "https://api-inference.huggingface.co/models/Lubna1/diagnoser_v1",
      {
        method: "POST",
        headers: {
          "Authorization": "Bearer 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", // Replace with your token
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ inputs: text })
      }
    );

    if (!response.ok) throw new Error("API request failed");
    
    const data = await response.json();
    const prediction = data[0][0]; // Assumes format: [[{label: "LABEL_X", score: 0.XX}]]
    
    const isAppendicitis = prediction.label === "LABEL_1";
    const confidence = (prediction.score * 100).toFixed(2);

    resultDiv.innerHTML = `
      Diagnosis: <span class="${isAppendicitis ? 'appendicitis' : 'other'}">
        ${isAppendicitis ? "Appendicitis" : "Other Abdominal Disease"}
      </span><br>
      Confidence: ${confidence}%
    `;
  } catch (error) {
    resultDiv.innerHTML = `Error: ${error.message}`;
  }
}
