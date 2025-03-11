import numpy as np

def receiveSpike(data):
    return [i for i in range(1, len(data)) if data[i] > data[i - 1]]

def getSpikeTiming(data):
    return np.nonzero(data)[0]

def compareArray(array1,array2):

    # Get indices where elements are not equal
    indices = np.where(array1 != array2)

    # Convert the indices to (x, y) pairs
    result = list(zip(indices[0], indices[1]))

    return result


v_path = "W:\int8\data2/28nm144k_33/soft_data/N_V.npy"
v_new = np.load(v_path)

v_path = "W:\int8\data3/28nm144k/soft_data/N_V.npy"
v_old = np.load(v_path)

print(1)
# s_path = "./tmp/soft_data/N_spike.npy"
# s = np.load(s_path)

# wacc1 = "./tmp/soft_data/N_wacc1.npy"
# wacc1 = np.load(wacc1)

# wacc2 = "./tmp/soft_data/N_wacc2.npy"
# wacc2 = np.load(wacc2)
# print('end')

# v_path = "./tmp/soft_data/N_V.npy"
# v = np.load(v_path)

# s_path = "./tmp/soft_data/N_spike.npy"
# s = np.load(s_path)

# wacc1 = "./tmp/soft_data/N_wacc1.npy"
# wacc1 = np.load(wacc1)

# wacc2 = "./tmp/soft_data/N_wacc2.npy"
# wacc2 = np.load(wacc2)
# print('end')

