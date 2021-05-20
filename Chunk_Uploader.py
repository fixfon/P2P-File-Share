import os
import socket
import json
from datetime import datetime

host_name = ''
host_port = 8000

uploader_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
uploader_socket.bind((host_name, host_port))
uploader_socket.listen(5)

current_path = os.getcwd()
chunk_folder_path = current_path + "/chunks"

print("Host is waiting for connection...\n")

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

    req_list = [requested_file_name, requested_file_size]
    req_list_json = json.dumps(req_list)
    downloader_socket.send(req_list_json.encode())

    with open(requested_file_path, 'rb') as uploading_file:
        read_bytes = uploading_file.read(10)
        downloader_socket.send(read_bytes)
        print("{} (size: {}) sending now...".format(requested_file_name, requested_file_size))
        while True:
            read_bytes = uploading_file.read(1024)
            if not read_bytes:
                break
            downloader_socket.send(read_bytes)
    uploading_file.close()
    downloader_socket.close()
    print("The file {} sent successfully.\n".format(requested_file_name))

    upload_log_file = os.getcwd() + "/upload_log.txt"

    with open(upload_log_file, 'a+') as upload_log:
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%d/%m/%Y %H:%M:%S")
        log_data = "Time: " + timestamp_str + " File Name: " + requested_file_name + " Request from: " + str(addr[0])
        upload_log.seek(0)
        old_data = upload_log.read()
        if len(old_data) > 0:
            upload_log.write("\n")
        upload_log.write(log_data)
    upload_log.close()
    print("Looking for another connection...")