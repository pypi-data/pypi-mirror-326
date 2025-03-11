

def get_addr(baseaddr,size):
    baseaddr += size
    return hex(baseaddr)

# IN KB
def get_index_size(nNeuron):
    return nNeuron *32/8/1024

def get_max_nConn(nNeuron):
    space_available = 1280+128-nNeuron *32/8/1024
    return space_available*1024/(256/8)

#input in B
def weight_size_to_nConn(size):
    nConn = size/(256/8)
    return nConn

#baseaddr = 0x30728000
# size = 32
# size *= 1024
# addr = get_addr(baseaddr,size)
# count = int(size/4/1024)
# print(addr)
# print(count)

# size = get_index_size(288*1024)
# nConn = get_max_nConn(288*1024)
# print(size)
# print(nConn)

nConn = weight_size_to_nConn(672*1024)
print(nConn)
