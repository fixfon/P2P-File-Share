# chunk_list = [1, 2, 3, 4]
# downloaded_chunk_list = []
#
# temp_ch_list = []
#
# for ch_file in chunk_list:
#     temp_ch_list.append(ch_file)
#     if ch_file != 4:
#         downloaded_chunk_list.append(ch_file)
#
#
# for dw_file in downloaded_chunk_list:
#     for ch_index in temp_ch_list:
#         if dw_file == ch_index:
#             chunk_list.remove(dw_file)
#
# print("Chunk List: ", chunk_list, "\n")
# print("Temp Chunk List: ", temp_ch_list, "\n")
# print("Downloaded Chunk List: ", downloaded_chunk_list, "\n")
#
# content_dict = {}
#
# if "forest_1" in content_dict:
#     content_dict["forest_1"].append("192.168.1.8")
# else:
#     content_dict["forest_1"] = ["192.168.1.8"]
#
# if "forest_1" in content_dict:
#     content_dict["forest_1"].append("192.168.1.9")
#
# print(content_dict)
#

# first_list = [1, 2, 3]
# first_dict = {1: "asd", 2: "bsc", 3: "dsa", 4: "rewf"}
#
# for i in range(len(first_list)):
#     if first_list[i] in list(first_dict.keys()):
#         print("Hello")