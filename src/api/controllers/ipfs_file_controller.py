import os

from flask import jsonify, send_file

from utils.base_definitions import ALLOWED_EXTENSIONS
from utils.ipfs_helper import IPFSHelper

BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))


class IPFSFileController:
    def __init__(self):
        self.ipfs_helper = IPFSHelper()

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def file_upload(self, request):
        if 'file' not in request.files:
            return jsonify({'message': 'No file uploaded'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'message': 'No file selected'}), 400

        if not self.allowed_file(file.filename):
            return jsonify({'message': 'Invalid file extension'}), 400

        file_full_path: str = os.path.join(BASE_DIR, f"../../../upload/{file.filename}")
        file.save(file_full_path)

        file_hash, file_name = self.ipfs_helper.upload_file(file_path=file_full_path)
        os.remove(file_full_path)

        return jsonify({
            'message': 'File uploaded successfully',
            'file_hash': file_hash,
            'file_name': file_name
        }), 200

    def file_download(self, request):
        hash_input: str = request.form.get('hashInput')
        self.ipfs_helper.download_file(file_hash=hash_input)

        file_full_path: str = os.path.join(BASE_DIR, f"../../../ipfs_files/{hash_input}")

        if os.path.exists(file_full_path):
            download_link: str = f"/v1/api/ipfs_file_event/{hash_input}"
            return jsonify({'download_link': download_link}), 200

        return jsonify({'message': "hash"}), 400

    def post(self, request, event_name):
        if event_name == "upload":
            return self.file_upload(request=request)

        if event_name == "download":
            return self.file_download(request=request)

        return jsonify({'message': 'upload or download args false/true...'}), 400

    @staticmethod
    def get(filename: str):
        # Provide the path to the file you want to download
        file_full_path: str = os.path.join(BASE_DIR, f"../../../ipfs_files/{filename}")

        try:
            return send_file(file_full_path, as_attachment=True)
        except Exception as e:
            return jsonify({'message': str(e)}), 400
