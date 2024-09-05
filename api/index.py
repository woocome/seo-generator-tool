from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from flask_cors import CORS
import os
import openai

load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

allowed_origins = [
    'http://127.0.0.1:5500',
    'https://seo-generation-tool.design.webflow.com',
    'https://seo-generation-tool.webflow.io',
    'https://*.webflow.io',
    'https://*.webflow.com',  # This allows all subdomains of example.com
]

CORS(app, resources={r"/generate-seo-title": {"origins": allowed_origins}})

# Set your OpenAI API key
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)
# Define a route to generate an SEO meta title
@app.route('/generate-seo-title', methods=['POST', 'GET'])
def generate_seo_title():
    data = request.json
    keyword = data.get('keyword', 'financial')
    type_ = data.get('type')
    
    if type_ not in ["Blog", "Landing Page"]:
        return jsonify({"error": f"Invalid input {type_}"}), 400
    
    # Define the prompt based on the type
    prompt = f"Generate an SEO-optimized meta title for a {type_} using the keyword '{keyword}'."

    # Generate SEO title using OpenAI
    chat = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an SEO expert."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )

    meta_title = chat.choices[0].message.content.strip()

    return jsonify({"meta_title": meta_title})

# Run the application
if __name__ == '__main__':
    app.run(debug=True)