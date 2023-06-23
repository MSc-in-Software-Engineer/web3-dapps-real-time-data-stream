import os

from flask import current_app as app, Response, render_template
from flask import request

from .views.home_view import HomeView

BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))


@app.route('/ipfs_video_feed/<file_hash>')
def ipfs_video_feed(file_hash):
    video_path = os.path.join(BASE_DIR, f'../../ipfs_files/{file_hash}')

    def generate():
        with open(video_path, 'rb') as video_file:
            while True:
                data = video_file.read(1024 * 1024)  # Read video data in chunks
                if not data:
                    break
                yield data

    return Response(generate(), mimetype='video/mp4')


@app.route("/", methods=["GET"])
def home():
    home_view = HomeView()

    if request.method == 'GET':
        return home_view.get()
