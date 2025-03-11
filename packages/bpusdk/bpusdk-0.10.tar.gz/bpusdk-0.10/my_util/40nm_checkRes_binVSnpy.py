import os
import sys

import numpy as np
# import matplotlib.pyplot as plt
import struct
import math
    
def bytes2float(v) -> float:
    return struct.unpack('<f', struct.pack('4B', *[v[0], v[1], v[2], v[3]]))[0]

import os
print(os.path.abspath('.'))

#hw_input_path = "./data/tmpRes"
#sw_s = np.load("./data/SW/N_spike.npy")
#save_path =  "./compare_ei"

# hw_output_path = "./upload/tmpRes96_SNN/ei_data_96k_0.5/compute1_00"
# sw_output_path = "./data/tmp96_SNN/soft_data"

hw_output_path = "./upload/tmpRes96_dt0.5_externalConn/ei_data_96k_0.5/compute1_00"
sw_output_path = "./data/tmp96_dt0.5_externalConn/soft_data"

# hw_output_path = "./upload/tmpRes96_SNN/ei_data_96k_0.5/compute1_00"
# sw_output_path = "./data/tmp96_SNN/soft_data"

sw_s = np.load(sw_output_path+"/N_spike.npy")
#sw_inpS = np.load(sw_output_path+"/N_inpS.npy")
scope = 96

total_num = 1024*scope
print(f"totla_num: {total_num}")
scale = 0.5
ex_num = int(total_num * scale)
ih_num = int(total_num * scale)
total_neu = ex_num + ih_num
step = 100

tmp_file = total_neu // 16385 + 1
neu_list = []
for i in range(tmp_file):
    neu_list.append(16384) if i != tmp_file-1 else neu_list.append(total_neu - i*16384)

sw_spike_count = []
hw_spike_count = []
time_count = []
hw_spike = []
hw_time = []
sw_spike = []
sw_time = []

for iStep in range(step):
    count = 0
    sw_count = int(np.sum(sw_s[iStep]))
    #sw_inpS_count = int(np.sum(sw_inpS[iStep]))
    for iFile in range(len(neu_list)):
        with open(os.path.join(hw_output_path, f"step{iStep + 1}", "spike_check", f"spike_check_{iFile}.bin"), "rb") as f_in:
            bin_data = f_in.read(4)
            sp_len = int.from_bytes(bin_data[0:4], byteorder='little', signed=False)
            sp_len = sp_len - 16384 * iFile if sp_len >= 16384 else sp_len
            for i in range(sp_len):
                bin_data = f_in.read(4)
                myint = int.from_bytes(bin_data, byteorder='little', signed=False)
                count += 1
                hw_spike.append(myint)
                hw_time.append(iStep)

    sw_spike_count.append(sw_count)
    hw_spike_count.append(count)
    time_count.append(iStep)
    print(f"iStep = {iStep}, hw_count = {count}, sw_count = {sw_count}, sw_inpS_count = {sw_count}")

# if plot == True:
#     plt.subplot(2,2,1)
#     plt.plot(time_count, hw_spike_count,'k.')

#     plt.subplot(2,2,2)
#     plt.plot(time_count, hw_spike_count,'r.')
#     #plt.plot(time, hw_spike,'k.')
#     plt.savefig('./count.png', bbox_inches='tight')
#     plt.close() 

#     plt.scatter(hw_time,hw_spike,s=1,color='g')
#     plt.savefig('./spike.png', bbox_inches='tight')

#print(hw_output_path)