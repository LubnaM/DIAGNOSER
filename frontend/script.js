async function diagnose() {
  const input = document.getElementById("inputText").value.trim();
  if (!input) {
    showError("Please describe symptoms");
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ inputs: input })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error || "API request failed");
    }

    const data = await response.json();
    displayResult(data);
  } catch (error) {
    showError(error.message);
  }
}

function displayResult(data) {
  // Adjust based on your model's response format
  const result = Array.isArray(data) ? data[0] : data;
  
  document.getElementById("prediction").textContent = 
    result.label === "LABEL_1" ? "Appendicitis" : "Other Condition";
  document.getElementById("confidence").textContent = 
    `${(result.score * 100).toFixed(2)}%`;
  document.getElementById("error").textContent = "";
}

function showError(message) {
  document.getElementById("error").textContent = message;
  document.getElementById("prediction").textContent = "--";
  document.getElementById("confidence").textContent = "--";
}
