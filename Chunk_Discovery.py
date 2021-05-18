import json
import os
from socket import *

serverPort = 5001
discoverySocket = socket(AF_INET, SOCK_DGRAM)
discoverySocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
discoverySocket.bind(('', serverPort))

print("Chunk Discovery is listening for chunk names...")

jsonAnnouncement, announcerAddress = discoverySocket.recvfrom(1024) #announcerAddress[0] = IP

print("An announcement received from ", announcerAddress, "\n")

chunk_filename_an = json.loads(jsonAnnouncement)
temp_list = list(chunk_filename_an.values())
chunk_file_names = temp_list[0]

current_path = os.getcwd()
file_name = 'content_dict.txt'
file_path = os.path.join(current_path, file_name)
content_dict = {}

if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    print("Looking for other chunk files and ip lists in the old content dictionary file...", "\n")
    with open(file_path, 'r') as read_file:
        content_dict = json.load(read_file)

with open(file_path, 'w') as content_file:
    for i in range(len(chunk_file_names)):

        if chunk_file_names[i] in content_dict.keys():
            ip_list = content_dict.get(chunk_file_names[i])

            if not announcerAddress[0] in ip_list:
                content_dict[chunk_file_names[i]].append(announcerAddress[0])

        else:
            content_dict[chunk_file_names[i]] = [announcerAddress[0]]

    json.dump(content_dict, content_file)

content_file.close()

print("Received chunk file list has been written and saved with ip address details in content dictionary file.", "\n")
print("All detected users and their hosted chunk list:", "\n")

host_chunk_dict = {}
host_ip_list = []

for garbage_ip_list in list(content_dict.values()):
    for i in range(len(garbage_ip_list)):
        if not garbage_ip_list[i] in list(host_chunk_dict.keys()):
            host_chunk_dict[garbage_ip_list[i]] = []

for ip_addr in list(host_chunk_dict.keys()):
    for chunk_n in list(content_dict.keys()):
        if ip_addr in content_dict.get(chunk_n):
            host_chunk_dict[ip_addr].append(chunk_n)

for keys, values in host_chunk_dict.items():
    print(keys, ":")
    print(values, "\n")
