import os
import socket
import json

host_name = ''
host_port = 8000

uploader_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
uploader_socket.bind((host_name, host_port))
uploader_socket.listen(5)

current_path = os.getcwd()
chunk_folder_path = current_path + "/chunks"

print("Host is waiting for connection...", "\n")

while True:
    downloader_socket, addr = uploader_socket.accept()
    print("Got connection from: {}".format(addr))

    requested_json = downloader_socket.recv(1024).decode()
    requested_dict = json.loads(requested_json)
    requested_file_name = str(requested_dict["requested_content"])
    print("A new request arrived. Requested file name: {}".format(requested_file_name))

    requested_file_path = ''

    for searched_path, searched_path_name, searched_path_file_name in os.walk(chunk_folder_path):
        if requested_file_name in searched_path_file_name:
            requested_file_path = os.path.join(searched_path, requested_file_name)

    requested_file_size = os.path.getsize(requested_file_path)
    print(requested_file_path, requested_file_size)
    req_list = [requested_file_name, requested_file_size]
    req_list_json = json.dumps(req_list)
    downloader_socket.send(req_list_json.encode())

    with open(requested_file_path, 'rb') as uploading_file:
        read_bytes = uploading_file.read(10)
        downloader_socket.send(read_bytes)
        while True:
            read_bytes = uploading_file.read(1024)
            if not read_bytes:
                downloader_socket.send(b'DONE SENDING')
                break
            downloader_socket.send(read_bytes)
    uploading_file.close()
    downloader_socket.close()
    print("Looking for another connection...")