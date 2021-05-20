import json
import os
import socket
import time
from datetime import datetime

program_value = True
downloaded_chunk_list = []

while program_value:  # Download different files.
    file_name = input("Enter the file name that you want to download (Ex: 'cutecat1.jpg'): ")
    file_name_wE = os.path.splitext(os.path.basename(file_name))[0]
    content_dict_path = os.getcwd() + "/content_dict.txt"
    file_chunk_list = []
    chunk_dict = {}
    missing_file = []

    for i in range(5):
        file_chunk_list.append(file_name_wE + "_" + str(i+1))

    with open(content_dict_path, 'r') as content_dict_file:
        content_dict = json.load(content_dict_file)
    content_dict_file.close()

    for i in range(len(file_chunk_list)):
        if not file_chunk_list[i] in content_dict.keys():
            missing_file.append(file_chunk_list[i])

    if len(missing_file) > 0:
        arg_value = True
        while arg_value:
            print("\n",
                  "No one has your requested chunk file '{}'.\nIf you proceed to download, you may encounter "
                  "missing file. "
                  "Do you want to enter another file name?".format(missing_file))
            cont_value = input("Enter 'Yes' or 'No': ")
            if cont_value == "No":
                program_value = False
                arg_value = False
                break
            elif cont_value == "Yes":
                arg_value = False
                break
            else:
                print("Please enter a valid argument.")

    else:
        for i in range(len(file_chunk_list)):
            chunk_dict[file_chunk_list[i]] = []
            chunk_dict[file_chunk_list[i]].extend(content_dict.get(file_chunk_list[i]))

        print("\nHosts that have your requested chunks:\n{}\n".format(chunk_dict))

        download_path = os.getcwd() + '/downloads'
        downloaded_file_folder = download_path + '/' + file_name_wE

        if not os.path.exists(download_path):
            try:
                os.mkdir(download_path)  # created downloaded file storage folder.
                print("A new folder 'downloads' has been created for store the downloaded files.")
            except OSError as error:
                print(error)

        if not os.path.exists(downloaded_file_folder):
            try:
                os.mkdir(downloaded_file_folder)  # created folder for downloaded file.
                print(
                    "A new folder {} has been created for store the downloaded file.\n".format(file_name_wE))
            except OSError as error:
                print(error)

        for downloading_chunk_name, ip_list in chunk_dict.items():

            downloading_chunk_path = downloaded_file_folder + "/" + downloading_chunk_name
            received_file_size = 0

            for ip_address in ip_list:
                # ############ TCP Session for downloading a chunk file. ############ #
                request_dict = {
                    "requested_content": downloading_chunk_name
                }

                host_name = ip_address
                host_port = 8000

                downloader_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    downloader_socket.connect((host_name, host_port))

                except socket.error as e:
                    if len(ip_list) > 1:
                        print("Could not connected with host {}. Will try with another host.\n".format(ip_address))
                        continue
                    else:
                        print("Could not connected with host {}. No host found for requested file.\n".format(ip_address))
                        continue

                print("Connection established with ", ip_address)
                request_json = json.dumps(request_dict)
                print("JSON Request: ", request_json)
                downloader_socket.send(request_json.encode())
                print("The file '{}' requested from host.\n".format(downloading_chunk_name))

                req_list_json = downloader_socket.recv(1024).decode()
                req_list = json.loads(req_list_json)

                received_file_name = req_list[0]
                received_file_size = req_list[1]
                print("'{}' (size: {}) is being downloaded...".format(received_file_name, received_file_size))

                with open(downloading_chunk_path, 'wb') as download_file:
                    received_bytes = downloader_socket.recv(10)
                    download_file.write(received_bytes)
                    while received_bytes:
                        try:
                            received_bytes = downloader_socket.recv(1024)
                        except socket.error as e:
                            print("Error receiving data:", e)
                            break
                        if received_bytes == b'':
                            break
                        download_file.write(received_bytes)
                download_file.close()
                if not os.path.getsize(downloading_chunk_path) == received_file_size:
                    if len(ip_list) < 2:
                        print("Downloading process of {} was not successful from {}. No one has your requested chunk "
                              "file. So program will stop, you can download another file by entering a new file name.\n".format(downloading_chunk_name, ip_address))
                    elif ip_address == ip_list[-1]:
                        print("Downloading process of {} was not successful from online peers. You can download "
                              "another file by entering a new file name.\n".format(downloading_chunk_name))
                    else:
                        print("Downloading process of {} was not successful from {}. Will try from another host.\n".format(downloading_chunk_name, ip_address))
                else:
                    print("{} downloaded successfully. Logged on 'download_log.txt' Moving on the next chunk file...".format(downloading_chunk_name))
                    print("***********************************************", "\n")
                    downloaded_chunk_list.append(downloading_chunk_name)
                    download_log_file = os.getcwd() + "/download_log.txt"
                    with open(download_log_file, 'a+') as download_log:
                        timestamp = datetime.now()
                        timestamp_str = timestamp.strftime("%d/%m/%Y %H:%M:%S")
                        log_data = "Time: " + timestamp_str + " File Name: " + downloading_chunk_name + " Host: " + str(ip_address)
                        download_log.seek(0)
                        old_data = download_log.read()
                        if len(old_data) > 0:
                            download_log.write("\n")
                        download_log.write(log_data)
                    download_log.close()
                    time.sleep(4)
                    break

                downloader_socket.close()

            if not os.path.getsize(downloading_chunk_path) == received_file_size:
                break

        if len(downloaded_chunk_list) == 5:
            # file_name  # this'll be the name of the content that user wanted to download from the network.
            # downloaded_chunk_list
            downloaded_file = downloaded_file_folder + "/" + file_name

            print("All chunks downloaded successfully. Chunks are being combined...")

            with open(downloaded_file, 'wb') as outfile:
                for chunk in downloaded_chunk_list:
                    downloaded_chunk_path = downloaded_file_folder + "/" + chunk
                    with open(downloaded_chunk_path, 'rb') as infile:
                        outfile.write(infile.read())
                    infile.close()
            outfile.close()
            print("The file {} was downloaded and combined successfully in {}\n".format(file_name, downloaded_file))

        new_bool = True
        while new_bool:
            new_download = input("Do you want to download another file? ('Yes' or 'No')")
            if new_download == 'Yes':
                new_bool = False
            elif new_download == 'No':
                new_bool = False
                program_value = False
            else:
                print("Please enter a valid argument.", "\n")
