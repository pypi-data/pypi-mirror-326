import numpy as np
import math
KB = 1024*8

def getIndexSize(nNeuron):
    size = nNeuron*32/KB
    return size

def size2nConn(size):
    nConn = size*KB/256 
    return nConn

nNeuron = 32*1024
print(f"nNeuron = {nNeuron}")
print(f"size = {getIndexSize(nNeuron)} KB")

size = 672
print(f"nNeuron = {nNeuron}")
print(f"size = {size2nConn(size)}")
