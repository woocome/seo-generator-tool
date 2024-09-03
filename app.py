from flask import Flask, request, jsonify
from openai import AsyncOpenAI
from flask_cors import CORS
import os

# Initialize the Flask application
app = Flask(__name__)
CORS(app, resources={r"/generate-seo-title": {"origins": "http://127.0.0.1:5500"}})

# Set your OpenAI API key
client = AsyncOpenAI(
  api_key="api_key"  # Replace with your actual API key
)

# Define a route to generate an SEO meta title
@app.route('/generate-seo-title', methods=['POST', 'GET'])
async def generate_seo_title():
    data = request.json
    keyword = data.get('keyword')
    type_ = data.get('type')
    
    if type_ not in ["Blog", "Landing Page"]:
        return jsonify({"error": f"Invalid input {type_}"}), 400
    
    # Define the prompt based on the type
    prompt = f"Generate an SEO-optimized meta title for a {type_} using the keyword '{keyword}'."

    # Generate SEO title using OpenAI
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an SEO expert."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )

    meta_title = response.choices[0].message['content'].strip()

    return jsonify({"meta_title": meta_title})

# Run the application
if __name__ == '__main__':
    app.run(debug=True)