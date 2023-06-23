import os

import ipfshttpclient

BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))


class IPFSHelper:
    __client: ipfshttpclient.Client = None

    def __init__(self):
        self.__connect_client()

    def __connect_client(self):
        # Connect to the local IPFS daemon
        self.__client: ipfshttpclient.Client = ipfshttpclient.connect()

    def upload_file(self, file_path: str) -> tuple:
        res = self.__client.add(file=file_path)
        _hash = res.get('Hash')
        _name = res.get('Name')
        return _hash, _name

    def download_file(self, file_hash: str) -> None:
        target: str = os.path.join(BASE_DIR, '../ipfs_files')
        self.__client.get(cid=file_hash, target=target)

    @staticmethod
    def remove_file_local(file_hash: str) -> None:
        target: str = os.path.join(BASE_DIR, f'../ipfs_files/{file_hash}')
        if os.path.exists(target):
            print(f"[INFO] - {file_hash} | file removed")
            os.remove(target)
            return

        print(f"[ERROR] - {file_hash} | file not found!")
        return
