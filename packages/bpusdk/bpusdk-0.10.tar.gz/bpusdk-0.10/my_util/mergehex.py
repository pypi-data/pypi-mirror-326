import os

def merge_hex(ori_dir, new_dir, name):
    ori_dir = ori_dir+'/'+name+'/'
    new_dir = new_dir+'/'+name+'/'
    os.makedirs(new_dir, exist_ok=True)
    
    path_list = os.listdir(ori_dir)
    for i in range(0,len(path_list)//4):
        path_list_local = path_list[i*4:i*4+4]
        outfile_path = new_dir+f"/{name}_tile_{i}.hex"
        with open(outfile_path, 'w') as outfile:
            for file_path in path_list_local:
                with open(ori_dir+file_path, 'r') as infile:
                    for line in infile:
                        outfile.write(line)

ori_dir = "./28nm576k/hex"
new_dir = "./28nm576k/hex_merged"

merge_hex(ori_dir, new_dir, "ncu")
merge_hex(ori_dir, new_dir, "index")
merge_hex(ori_dir, new_dir, "weight")
print(f"Files have been merged")
