import socket
from tkinter import filedialog
import os
import math
import json
import time

file_path = filedialog.askopenfilename()
file_name = file_path.split('/')[-1]
file_name_wE = os.path.splitext(os.path.basename(file_path))[0]
file_size = os.path.getsize(file_path)
chunk_size = math.ceil(math.ceil(file_size) / 5)
current_path = os.getcwd()
chunk_folder_path = current_path + "/chunks"
folder_path = chunk_folder_path + "/" + file_name_wE

print("***********************************************", "\n")

print(file_name, " the file is being divided into chunks...", "\n")

index = 0
namelist_chunk = []

with open(file_path, 'rb') as infile:
    chunk = infile.read(int(chunk_size))

    try:
        os.mkdir(chunk_folder_path)  # created chunk storage folder.
        print("A new folder 'chunks' has been created for store the different files chunks.", "\n")
    except OSError as error:
        print(error)

    try:
        os.mkdir(folder_path)  # created folder for every chunk file.
        print("A new folder {} has been created for store the chunk files.".format(file_name_wE), "\n")
    except OSError as error:
        print(error)

    print("***********************************************", "\n")

    while chunk:
        chunk_name = file_name_wE + '_' + str(index + 1)
        namelist_chunk.append(chunk_name)
        chunk_path = os.path.join(folder_path, chunk_name)

        with open(chunk_path, 'wb+') as chunk_file:
            chunk_file.write(chunk)
        print("Chunk #{} has been created.".format(index + 1))
        index += 1
        chunk = infile.read(int(chunk_size))
        chunk_file.close()
infile.close()

print("The file '", file_name, "' has divided into 5 chunks of each ", chunk_size, " bytes.", "\n")
print("***********************************************", "\n")
print("Searching for other chunk files in directory: ", chunk_folder_path, "\n")

chunk_folder_list = []
chunk_folder_inside = []
chunk_dictionary = {}

first_element = True

index2 = 0

for searched_path, searched_path_name, searched_path_file_name in os.walk(chunk_folder_path):
    if first_element:
        chunk_folder_list = searched_path_name
        first_element = False
    else:
        chunk_folder_inside = searched_path_file_name
        chunk_dictionary[chunk_folder_list[index2]] = chunk_folder_inside
        index2 += 1

print("Found {} different files.".format(len(chunk_folder_list)))
print("Founded file list: ")

print(chunk_folder_list, "\n")

print("***********************************************", "\n")

print("Existing chunk list is being turned into JSON format...", "\n")

chunk_file_list = []

for ch_lists in chunk_dictionary.values():
    for ch_names in ch_lists:
        chunk_file_list.append(ch_names)

announcement_dict = {
    "chunks": chunk_file_list
}

json_Announcement = json.dumps(announcement_dict)

print("JSON Announcement: ", "\n", "\n", json_Announcement, "\n")

print("***********************************************", "\n")

# ######### UDP CLIENT CONNECTION ##########

serverIP = '192.168.1.255'
serverPort = 5001
serverAddress = (serverIP, serverPort)
index_broadcast = 0

announcementSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
announcementSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("Starting to broadcast chunks...", "\n")

while True:
    announcementSocket.sendto(json_Announcement.encode('utf-8'), serverAddress)

    print("Broadcasted {} times. Still keeping on...".format(index_broadcast), "\n")
    index_broadcast += 1
    time.sleep(8)
