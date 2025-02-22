from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "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"
API_URL = "https://api.perplexity.ai/chat/completions" 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form.get("question")
    
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {"query": user_question}
    
    response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to get a response"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
