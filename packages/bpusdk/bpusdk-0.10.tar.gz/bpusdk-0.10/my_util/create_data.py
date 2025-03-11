
import os
new_dir = "./00"
os.makedirs(new_dir, exist_ok=True)

size_list = [128,4*1024,8*1024,16*1024,32*1024,64*1024,128*1024,1280*1024]
name_list = ["/128B.bin","/4KB.bin","/8KB.bin","/16KB.bin","/32KB.bin","/64KB.bin","/128KB.bin","/1280KB.bin"]

for i in range(len(size_list)):
    file_size = size_list[i]
    file_name = name_list[i]
    outfile_path = new_dir+file_name
    with open(outfile_path, "wb") as f:
        f.write(bytearray([0x00] * file_size))






