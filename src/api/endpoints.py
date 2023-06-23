from flask import current_app as app, request, jsonify

from .controllers.home_controller import HomeController
from utils.base_definitions import API_PREFIX
from .controllers.ipfs_file_controller import IPFSFileController

ipfs_file_controller: IPFSFileController = IPFSFileController()


@app.route(f'{API_PREFIX}/ipfs_file_event/<event_name>', methods=['POST'])
@app.route(f'{API_PREFIX}/ipfs_file_event/<filename>', methods=['GET'])
def file_upload(filename="", event_name=""):
    if request.method == 'GET':
        return ipfs_file_controller.get(filename=filename)

    elif request.method == 'POST':
        return ipfs_file_controller.post(request=request, event_name=event_name)

    return jsonify({'status': False, 'message': 'Method Not Allowed! ... [GET, POST] only REQUEST ACCEPTABLE!'}), 405


@app.route(f'{API_PREFIX}/', methods=['GET'])
def home_api():
    home_controller = HomeController()

    if request.method == 'GET':
        return home_controller.get()

    return jsonify({'status': False, 'message': 'Method Not Allowed! ... [GET] only REQUEST ACCEPTABLE!'}), 405
