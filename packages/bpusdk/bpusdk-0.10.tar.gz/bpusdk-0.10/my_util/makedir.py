
import os 
#uploadPath = "./Res28nm576k_coba_dt10_int8"
uploadPath = "../upload5/Res28nm64k_mode2"
step_num = 20

# for i in range(0, step_num + 1):
#     os.makedirs(f'{uploadPath}/step' + str(i) +
#                 '/index_check', exist_ok=True)
    
# for i in range(0, step_num + 1):
#     os.makedirs(f'{uploadPath}/step' + str(i) +
#                 '/weight_check_new', exist_ok=True)
    
for i in range(0, step_num + 1):
    os.makedirs(f'{uploadPath}/step' + str(i) +
                '/weight_check', exist_ok=True)
    
for i in range(0, step_num + 1):
    os.makedirs(f'{uploadPath}/step' + str(i) +
                '/spike_check', exist_ok=True)
print(1)