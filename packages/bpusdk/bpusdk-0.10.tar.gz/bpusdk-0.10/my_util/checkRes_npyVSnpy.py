import numpy as np

def returnMaxMin(x):
    return np.max(x), np.min(x)

def removeCommon(list_a,list_b):
    common_elements = set(list_a) & set(list_b)
    list_a = [item for item in list_a if item not in common_elements]
    list_b = [item for item in list_b if item not in common_elements]
    return list_a, list_b


def find_change_indices(data):
    return [i for i in range(1, len(data)) if data[i] > data[i - 1]]


# hw_output_path = "Res28nm144k_new"
# sw_output_path = "./28nm144k_new/soft_data"

nTile = 36
nNpu =nTile*4
hw_output_path = "../upload/Res28nm576k"
sw_output_path = "../data/28nm576k/soft_data"

nStep = 20

hw_s     = np.load(hw_output_path+"/hw_s.npy").astype(np.int32) 
hw_v     = np.load(hw_output_path+"/hw_v.npy").astype(np.float32)
hw_wacc1 = np.load(hw_output_path+"/hw_wacc1.npy").astype(np.float32)
hw_wacc1 = hw_wacc1*(1/0.8)
# hw_wacc2 =np.load(hw_output_path+"/hw_wacc2.npy").astype(np.float32)
sw_s     = np.load(sw_output_path+"/N_spike.npy").astype(np.int32) 
sw_v     = np.load(sw_output_path+"/N_V.npy").astype(np.float32)
# sw_inpS     = np.load(sw_output_path+"/N_inpS.npy").astype(np.int32) 
sw_wacc1 = np.load(sw_output_path+"/N_wacc1.npy").astype(np.float32)
# sw_wacc2 =np.load(sw_output_path+"/N_wacc2.npy").astype(np.float32)

# hw_wacc1 = np.roll(hw_wacc1, 1,axis=0)
# hw_wacc2 = np.roll(hw_wacc2, 1,axis=0)

for iStep in range(nStep):
    hw_count = int(np.sum(hw_s[iStep]))
    hw_s_loc = np.nonzero(hw_s[iStep])[0]
    hw_v_loc = hw_v[iStep]
    hw_wacc1_loc = hw_wacc1[iStep]
    # hw_wacc2_loc = hw_wacc2[iStep]

    sw_count = np.sum(sw_s[iStep])
    sw_s_loc = np.nonzero(sw_s[iStep])[0]

    sw_v_loc = sw_v[iStep]
    sw_wacc1_loc = sw_wacc1[iStep]
    #sw_wacc2_loc = sw_wacc2[iStep]
    
    s_comp = np.array_equal(hw_s_loc, sw_s_loc)
    hw_s_loc_unique,sw_s_loc_unique =  removeCommon(hw_s_loc, sw_s_loc)
    v_diff = np.abs(hw_v_loc-sw_v_loc)
    ii = np.argmax(v_diff)


    wacc_diff = np.abs(hw_wacc1_loc-sw_wacc1_loc)
    i_wacc_diff = np.argmax(wacc_diff)

    flag = np.array_equal(sw_s_loc, hw_s_loc)
    print(f"iStep = {iStep}, flag = {flag}, hw_count = {hw_count},sw_count = {sw_count}")
    print(f"iStep = {iStep}, v_comp_max = {np.max(v_diff)}, ii={ii}")
    #print(f"iStep = {iStep}, wacc_comp_mean = {np.mean(wacc_diff)}, wacc_comp_max = {np.max(wacc_diff)}, ii={i_wacc_diff}")
    
    npu_check = []
    v_diff_list = []
    for iNpu in range(nNpu):
        istart = iNpu*4096
        iend = (iNpu+1)*4096
        sw_v_loc = sw_v[iStep,istart:iend] 
        hw_v_loc = hw_v[iStep,istart:iend]
        v_diff = np.abs(hw_v_loc-sw_v_loc)
        v_diff_list.append(np.max(v_diff))
        if np.max(v_diff)<=1E-3 :
            npu_check.append(1)
        else:
            npu_check.append(0)

    # print(f"iStep = {iStep}, npu_check = {npu_check}")

    if np.max(v_diff)>=1E-3 :
        tmp = np.nonzero(wacc_diff)[0]
        tmp1 = np.nonzero(v_diff)[0]
        filtered = [num for num in tmp1 if 4*4096 < num  < 5*4096]
        print("----------------------------------ERROR-----------------------------------------------------")


hw = find_change_indices(hw_wacc1[:,0]) 
sw = find_change_indices(sw_wacc1[:,0]) 
# tmp = np.concatenate((hw_wacc1[:,7],sw_wacc1[:,7]),axis=1)

print("end")
