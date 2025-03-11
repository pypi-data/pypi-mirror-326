import brainpy as bp
import brainpy.math as bm
import numpy as np
import matplotlib.pyplot as plt
from brainpy.neurons import LIF
from brainpy.synapses import Exponential
import time
np.random.seed(42)
bm.random.seed(42)
weight = 1.

tot_num = 512*1024

num_exc = int(tot_num/2)
num_inh = int(tot_num/2)
connect_prob = 5 / tot_num
allow_multi_conn = True
method='exp_auto'

E_pars = dict(V_rest=-60., V_th=-50.,
                V_reset=-60., tau=20., tau_ref=5.)
I_pars = dict(V_rest=-60., V_th=-50.,
                V_reset=-60., tau=20., tau_ref=5.)

E = LIF(num_exc, **E_pars, method=method)
I = LIF(num_inh, **I_pars, method=method)

# 固定所有膜电位初始值为-60
E.V.value = bp.math.zeros(num_exc) - 60.
I.V.value = bp.math.zeros(num_inh) - 60.

# synapses
w_e = 0.8187  # excitatory synaptic weight
w_i = 0.9048  # inhibitory synaptic weight
E_pars = dict(output=bp.synouts.COBA(E=0.), g_max=w_e, tau=5.)
I_pars = dict(output=bp.synouts.COBA(E=-80.), g_max=w_i, tau=10.)




# Neurons connect to each other randomly with a connection probability of 2%
E2E = Exponential(E, E, bp.conn.FixedProb(prob=connect_prob, allow_multi_conn=allow_multi_conn), **E_pars, method=method)
E2I = Exponential(E, I, bp.conn.FixedProb(prob=connect_prob, allow_multi_conn=allow_multi_conn), **E_pars, method=method)
I2E = Exponential(I, E, bp.conn.FixedProb(prob=connect_prob, allow_multi_conn=allow_multi_conn), **I_pars, method=method)
I2I = Exponential(I, I, bp.conn.FixedProb(prob=connect_prob, allow_multi_conn=allow_multi_conn), **I_pars, method=method)

pre_size = (4, 4)
post_size = (3, 3)

uniform_init = bp.init.Uniform(min_val=0., max_val=1.)
weights = uniform_init((np.prod(pre_size), np.prod(post_size)))
print('shape of weights: {}'.format(weights.shape))

#conn = bp.conn.FixedProb(prob=0.05, allow_multi_conn=True)
#conn()

t0 = time.time()
conn_mat_E2E = E2E.conn.requires('pre2post')  # request the connection matrix
conn_mat_E2I = E2I.conn.requires('pre2post')  # request the connection matrix
conn_mat_I2E = I2E.conn.requires('pre2post')  # request the connection matrix
conn_mat_I2I = I2I.conn.requires('pre2post')  # request the connection matrix

t1 = time.time()
print('Initial Brainpy Network. Elapsed: %.2f s\n' %(t1-t0))  #输出

'''
i, j = (2, 3)
print('whether (i, j) is connected: {}'.format(conn_mat_E2E[i, j]))
print('synaptic weights of (i, j): {}'.format(weights[i, j]))
'''