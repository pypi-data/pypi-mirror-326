import numpy as np
import pickle 
from collections import defaultdict

with open('../data4/28nmtmp\soft_data\connection.pickle', 'rb') as handle:
    new = pickle.load(handle)

def get_id(x):
    x_global = x
    nNpu = 1024*4*4
    nTile = nNpu*4
    iTile = int(np.floor(x/nTile))
    x -=iTile*nTile
    iNpu = int(np.floor(x/nNpu))
    x -= iNpu*nNpu
    # print(f"x_global: {x_global}, x_local: {int(x)}")
    # print(f"iTile:{iTile}")
    # print(f"iNpu:{iNpu}")
    return [x_global, x,iTile,iNpu,x_global%4]


pre_list = []
post_list = []
for key in new:
    value_list = new[key]
    for value in value_list:
        pre_list.append(key)
        post_list.append(value)

pre_list = np.array(pre_list)
post_list = np.array(post_list)
print(1)

indices = np.where(post_list == 0)
print(pre_list[indices])
print(post_list[indices])
print(len(pre_list[indices]))

# get_id(151188)

# def removeCommon(list_a,list_b):
#     common_elements = set(list_a) & set(list_b)
#     # Remove common elements from both lists
#     list_a = [item for item in list_a if item not in common_elements]
#     list_b = [item for item in list_b if item not in common_elements]
#     return list_a, list_b
# # nStep, nNeuron = hw_s.shape

print(1)