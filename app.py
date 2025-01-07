git init
from flask import Flask, render_template, request, redirect, url_for, jsonify
from base64 import b64encode  # Pastikan impor ini ada
import requests
import os


app = Flask(__name__)

# Ganti dengan API Key Clarifai Anda
CLARIFAI_API_KEY = '4eb3ddfd535a4647ade15a96e1362040'
CLARIFAI_URL = 'https://api.clarifai.com/v2/models/general-image-recognition/outputs'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Ambil file gambar dari form
    image = request.files['image']

    # Ubah file gambar ke base64
    image_data = image.read()
    encoded_image = image_data.encode('base64') if hasattr(image_data, 'encode') else b64encode(image_data).decode()

    # Kirim ke API Clarifai
    headers = {
        'Authorization': f'Key {CLARIFAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "inputs": [
            {
                "data": {
                    "image": {
                        "base64": encoded_image
                    }
                }
            }
        ]
    }
    response = requests.post(CLARIFAI_URL, headers=headers, json=data)

    # Proses hasil
    if response.status_code == 200:
        concepts = response.json()['outputs'][0]['data']['concepts']
        return jsonify(concepts)
    else:
        return jsonify({'error': 'Failed to process image'}), 500

if __name__ == '__main__':
    app.run(debug=True)

