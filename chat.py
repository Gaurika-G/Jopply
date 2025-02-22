import re
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "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"  # Replace with your real API key
API_URL = "https://api.perplexity.ai/chat/completions"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form.get("question")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "sonar-pro",  # Use a valid model (Perplexity's recommended models)
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_question}
        ]
    }

    response = requests.post(API_URL, json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        answer = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        return jsonify({"answer": answer})
    else:
        return jsonify({"error": "Failed to get a response", "details": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
