import numpy as np
import struct
from tqdm import tqdm

nTile = 9
nStep = 20
hw_output_path = ".\Res28nm144k_new"
init_path = "./28nm144k_new/144k_split1_base1/ncu"
sw_output_path = "./28nm144k_new/soft_data"

nStep = 20

sw_s     = np.load(sw_output_path+"/N_spike.npy").astype(np.int32) 
sw_v     = np.load(sw_output_path+"/N_V.npy").astype(np.float32)

nNeuron_in_npu = 1024*4
nNpu_in_tile = 4

def bytes2float(v) -> float:
    return struct.unpack('f', struct.pack('4B', *[v[0], v[1], v[2], v[3]]))[0]

def replace_hexadecimal_value(value):
    return 1 if value == 129 else 0  #129 == \x81, 0 ==\x00


def split_data_in_rows(data, columns):
    rows = int(len(data)/columns)
    return [data[i*columns : (i+1)*columns] for i in range(rows)]


def read_file(filename, columns):
    with open(filename, 'rb') as file:
        data = file.read()
    data = [replace_hexadecimal_value(x) for x in data]
    data = split_data_in_rows(data, columns)
    data = np.array(data)
    tmp = []
    for i in range(8):
        tmp.extend(data[:512,i])
    return tmp

nNeuron= nTile*nNpu_in_tile*nNeuron_in_npu
hw_s, hw_v  = np.zeros([nStep, nNeuron], dtype=float), np.zeros([nStep, nNeuron], dtype=float)

for iDie in range(1):
    test_pass = True
    for iStep in tqdm(range(nStep)):
        for iTile in range(nTile):
            for iNpu in range(nNpu_in_tile):
                offset = iTile * nNeuron_in_npu*nNpu_in_tile + iNpu * nNeuron_in_npu
                iTile_load = iTile+iDie*9
                path = f"{hw_output_path}/step{iStep}/weight_check/weight_check_tile{iTile_load}_npu{iNpu}.bin"
                if iStep == 0:
                    path= f"{init_path}/ncu_tile{iTile}_npu{iNpu}.bin"
                with open(path, "rb") as f_in:
                    for i in range(nNeuron_in_npu):
                        f_in.read(4*5) 
                        hw_v[iStep, i+offset] = bytes2float(f_in.read(4)) 
                        f_in.read(4*2)
                
                if iStep > 0:
                    path = f"{hw_output_path}/step{iStep}/spike_check/spike_check_tile{iTile}_npu{iNpu}.bin"
                    with open(path, "rb") as f_in:
                        columns = 8
                        nNeuron_in_NPU = 4096
                        data = read_file(path, columns)
                        hw_s[iStep, offset:offset+nNeuron_in_NPU] = data
                        nSpikes = sum(data)

        hw_v_loc = hw_v[iStep]
        sw_v_loc = sw_v[iStep]
        v_diff = np.abs(hw_v_loc-sw_v_loc)
        flag = np.array_equal(np.nonzero(sw_s[iStep])[0], np.nonzero(hw_s[iStep])[0])
        if flag == False or np.max(v_diff)>0.01:
            test_pass = False

    if test_pass:
        print(f"Test PASS for Die {iDie}")
    else:
        print(f"Test FAIL for Die {iDie}")

