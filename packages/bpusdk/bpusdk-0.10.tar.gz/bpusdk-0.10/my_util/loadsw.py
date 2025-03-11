import numpy as np



sw_output_path = "./28nm576k_coba_dt10_int8/soft_data"

nStep = 20
sw_s     = np.load(sw_output_path+"/N_spike.npy").astype(np.int32) 
sw_v     = np.load(sw_output_path+"/N_V.npy").astype(np.float32)
sw_wacc1 = np.load(sw_output_path+"/N_wacc2.npy").astype(np.float32)

for iStep in range(nStep):
    sw_count = np.sum(sw_s[iStep])
    sw_s_loc = np.nonzero(sw_s[iStep])[0]

    sw_v_loc = sw_v[iStep]
    sw_wacc1_loc = sw_wacc1[iStep]
 
    print(f"iStep = {iStep}, sw_count = {sw_count}")
   