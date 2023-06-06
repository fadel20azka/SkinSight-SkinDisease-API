from flask import Flask, request, jsonify, send_file
from google.cloud import storage
import tensorflow as tf
import numpy as np
import tensorflow.keras as keras

app = Flask(__name__)
bucket_name = "skin_desease"  # Replace with your actual bucket name

@app.route('/api/upload/<uid>', methods=['POST'])
def upload_skin_picture(uid):
    try:
        if 'file' not in request.files:
            response = jsonify({
                'status': 'Failed',
                'message': 'Tidak ada file yang ditambahkan'
            })
            response.status_code = 400
            return response

        file = request.files['file']
        file_name = file.filename
        blob = storage.Client().bucket(bucket_name).blob(file_name)

        if blob.exists():
            blob.delete()

        blob.upload_from_file(file, content_type='application/octet-stream')
    
        # Add code here to update the user document with the public_url

        response = jsonify({
            'status': 'Success',
            'message': 'Skin picture berhasil ditambahkan'
        })
        response.status_code = 200
        return response

    except Exception as error:
        print(error)  # Log the error for debugging purposes

        response = jsonify({
            'status': 'Failed',
            'message': 'An internal server error occurred',
            'error': str(error)
        })
        response.status_code = 500
        return response

# Load the TFLite model
