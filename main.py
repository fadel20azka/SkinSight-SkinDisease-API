from flask import Flask, request, jsonify, send_file
from google.cloud import storage

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

        public_url = f"https://storage.googleapis.com/skin_desease/skinpict"
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

@app.route('/api/picture/<uid>', methods=['GET'])
def get_picture(uid):
    try:
        blob = storage.Client().bucket(bucket_name).blob(f"{uid}.h5")
        if not blob.exists():
            response = jsonify({
                'status': 'Failed',
                'message': 'File not found'
            })
            response.status_code = 404
            return response

        # Download the H5 file from the blob
        temp_file_path = f'/path/to/temp/{uid}.h5'  # Provide a temporary file path
        blob.download_to_filename(temp_file_path)

        # Add code here to extract the image from the H5 file and save it as a separate image file
        image_file_path = f'/path/to/temp/{uid}.jpg'  # Provide a file path to save the extracted image
        # Extract the image from the H5 file and save it as a separate image file
        # Make sure to replace this code with the actual logic to extract the image from the H5 file

        # Send the image file as a response
        return send_file(image_file_path, mimetype='image/jpeg')

    except Exception as error:
        print(error)  # Log the error for debugging purposes

        response = jsonify({
            'status': 'Failed',
            'message': 'An internal server error occurred',
            'error': str(error)
        })
        response.status_code = 500
        return response

if __name__ == '__main__':
    app.run()