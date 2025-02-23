import re
import json
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace with your actual API key
API_KEY = "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"
API_URL = "https://api.perplexity.ai/chat/completions"

@app.route('/')
def home():
    return render_template('index.html')

# AI Chatbot Route (Chat functionality from chat.py)
@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form.get("question")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "sonar-pro",
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

# AI Cover Letter Generator Route (Functionality from app.py)
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json  

    # Extract user input
    name = data.get("name", "Your Name")
    email = data.get("email", "your.email@example.com")
    experiences = ", ".join(data.get("experiences", []))
    skills = data.get("skills", "")
    education = data.get("education", "")
    hackathons = ", ".join(data.get("hackathons", []))
    projects = ", ".join(data.get("projects", []))
    job_title = data.get("job_title", "a job")
    company = data.get("company", "a company")
    job_desc = data.get("job_description", "")
    location = data.get("location", "")

    # Send request to Perplexity AI
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": "You are an AI cover letter generator."},
            {"role": "user", "content": f"Write a professional cover letter for {job_title} at {company} in {location}. Job description: {job_desc}. "
                                        f"User's background: Name: {name}, Email: {email}, Education: {education}, Skills: {skills}, "
                                        f"Experience: {experiences}, Hackathons: {hackathons}, Projects: {projects}."}
        ]
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        cover_letter = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        return cover_letter.replace("\\n", "\n")
    else:
        return "Failed to generate cover letter."



if __name__ == '__main__':
    app.run(debug=True)
