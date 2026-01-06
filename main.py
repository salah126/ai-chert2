import os
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY not set"}), 500

    client = genai.Client(api_key=api_key)
    question = request.form.get("question", "Explain AI shortly")

    file = request.files.get("image")
    if file:
        image_bytes = file.read()
        content = [
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=file.mimetype
            ),
            question
        ]
    else:
        content = question

    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=content
        )
        answer = response.text
    except Exception as e:
        return jsonify({"error": f"{str(e)}"})

    return jsonify({"answer": answer})
