import numpy as np
import struct
import math 

scope = 576
hw_output_path = "Res28nm576k_int8"
init_path = "./28nm576k_int8/576k_split1_base1/ncu"

nStep = 20

scale = 4
nNeuron= scope*1024
nTile = int(scope/16/scale)
nNeuron_in_npu = 4096*scale
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
        tmp.extend(data[:2048,i])
    # data = [x[::-1] for x in data]
    # data = [byte for row in data for byte in row]
    #print(1)
    return tmp

hw_spike, hw_v, hw_wacc1, hw_wacc2,  = np.zeros([nStep, nNeuron], dtype=float), np.zeros([nStep, nNeuron], dtype=float), np.zeros([nStep, nNeuron], dtype=float), np.zeros([nStep, nNeuron], dtype=float)

for iStep in range(0,nStep):
    print(f"iStep: {iStep}")
    for iTile in range(nTile):
        for iNpu in range(nNpu_in_tile):
            offset = iTile * nNeuron_in_npu*nNpu_in_tile + iNpu * nNeuron_in_npu
            
            path = f"{hw_output_path}/step{iStep}/weight_check/weight_check_tile{iTile}_npu{iNpu}.bin"
            if iStep == 0:
                path= f"{init_path}/ncu_tile{iTile}_npu{iNpu}.bin"
            with open(path, "rb") as f_in:
                for i in range(0,nNeuron_in_npu,4):
                    
                    tmp = f_in.read(4*4) 
                    hw_wacc1[iStep, i+offset+0] =  int.from_bytes(f_in.read(1), byteorder='little', signed=True)
                    hw_wacc1[iStep, i+offset+1] =  int.from_bytes(f_in.read(1), byteorder='little', signed=True)
                    hw_wacc1[iStep, i+offset+2] =  int.from_bytes(f_in.read(1), byteorder='little', signed=True)
                    hw_wacc1[iStep, i+offset+3] =  int.from_bytes(f_in.read(1), byteorder='little', signed=True)        

                    hw_v[iStep, i+offset+0] =  int.from_bytes(f_in.read(1), byteorder='little', signed=True)
                    hw_v[iStep, i+offset+1] =  int.from_bytes(f_in.read(1), byteorder='little', signed=True)
                    hw_v[iStep, i+offset+2] =  int.from_bytes(f_in.read(1), byteorder='little', signed=True)
                    hw_v[iStep, i+offset+3] =  int.from_bytes(f_in.read(1), byteorder='little', signed=True)        
                    
                    tmp = f_in.read(4*2)
    
            if iStep > 0:
                path = f"{hw_output_path}/step{iStep}/spike_check/spike_check_tile{iTile}_npu{iNpu}.bin"
                with open(path, "rb") as f_in:
                    columns = 8
                    nNeuron_in_NPU = 4096*4
                    data = read_file(path, columns)
                    hw_spike[iStep, offset:offset+nNeuron_in_NPU] = data
                    nSpikes = sum(data)


np.save(hw_output_path+"/hw_s.npy",hw_spike)
np.save(hw_output_path+"/hw_v.npy",hw_v)
np.save(hw_output_path+"/hw_wacc1.npy",hw_wacc1)
# np.save(hw_output_path+"/hw_wacc2.npy",hw_wacc2)



