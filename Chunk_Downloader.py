import json
import os
import socket

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

        print("\n", "Hosts that have your requested chunks: \n", chunk_dict)

        download_path = os.getcwd() + '/downloads'
        downloaded_file_folder = download_path + '/' + file_name_wE

        if not download_path:
            try:
                os.mkdir(download_path)  # created downloaded file storage folder.
                print("A new folder 'downloads' has been created for store the downloaded files.", "\n")
            except OSError as error:
                print(error)

        if not downloaded_file_folder:
            try:
                os.mkdir(downloaded_file_folder)  # created folder for downloaded file.
                print(
                    "A new folder {} has been created for store the downloaded file.".format(file_name_wE),
                    "\n")
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
                host_port = 5001

                downloader_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                downloader_socket.connect((host_name, host_port))

                print("Connection established with ", ip_address)

                request_json = json.dumps(request_dict)

                print("JSON Request: ", request_json)

                downloader_socket.send(request_json.encode())
                print("The file '{}' requested from host.".format(downloading_chunk_name))

                received_file_name, received_file_size = downloader_socket.recv(1024).decode()
                print("'{}' (size: {}) is being downloaded...".format(received_file_name, received_file_size))

                with open(downloading_chunk_path, 'wb+') as download_file:
                    while True:
                        try:
                            received_bytes = downloader_socket.recv(1024)
                            download_file.write(received_bytes)
                        except socket.error as e:
                            print("Error receiving data:", e)
                            break
                        if not received_bytes:
                            break
                download_file.close()
                if os.path.getsize(downloading_chunk_path) != received_file_size:
                    if len(ip_list) < 2:
                        print("Downloading process of {} was not successful from {}. No one has your requested chunk "
                              "file. So program will stop, you can download another file by entering a new file name."
                              " ")
                    elif ip_address == ip_list[-1]:
                        print("Downloading process of {} was not successful from online peers. You can download "
                              "another file by entering a new file name.")
                    else:
                        print("Downloading process of {} was not successful from {}. Will try from another host.")
                else:
                    print("{} downloaded successfully. Moving on the next chunk file...".format(downloading_chunk_name))
                    downloaded_chunk_list.append(downloading_chunk_name)
                    # download log burada oluşturulacak.
                    break

            if os.path.getsize(downloading_chunk_path) != received_file_size:
                break

        if len(downloaded_chunk_list) == 5:
            # file_name  # again, this'll be the name of the content that used wanted to download from the network.
            # downloaded_chunk_list
            downloaded_file_path = downloaded_file_folder + file_name

            with open(downloaded_file_path, 'wb') as outfile:
                for chunk in downloaded_chunk_list:
                    downloading_chunk_path = downloaded_file_path + chunk
                    with open(downloading_chunk_path, 'rb') as infile:
                        outfile.write(infile.read())
                    infile.close()
            outfile.close()
