
from brainpy._src.integrators import odeint, sdeint, JointEq
import brainpy as bp
import numpy as np
import matplotlib.pyplot as plt
import jax

def generated_function1(a, b, c):
    d = jax.lax.neg(b)
    e = d.astype(jax.numpy.float32)
    f = e + jax.numpy.float64(-60.0)
    g = jax.numpy.float64(1.0) * a
    h = f + g
    i = h / jax.numpy.float64(20.0)
    j = c * -0.05000000074505806
    k = abs(j)
    l = k <= 9.999999747378752e-06
    m = j / 2.0
    n = 1.0 + m
    o = j * j
    p = o / 6.0
    q = n + p
    r = jax.numpy.exp(j)
    s = r - 1.0
    t = s / j
    u = jax.lax.select_n(l, t, q)
    v = c * u
    w = v * i
    x = b.astype(jax.numpy.float32)
    y = x + w
    return y

def derivative1(V, t, I):
    V_rest = np.array(-60.)
    R = np.array(1.)
    tau = np.array(20.)
    dv = (-V + V_rest + R * I) / tau
    return dv

def derivative2(g, t):
    tau = 5.
    dg = -g / tau
    return dg

def step_run1(V,dt):
    I = np.array(20.)
    #V = integral(V, t, I, dt) 
    V = generated_function1(V, t, I,)
    return V

def step_run2(g,dt):
    g = integral(g, t, dt) 
    return g

#------------------- Case 1 ---------------------------------------
integral = odeint(method="exp_auto", f=derivative1,show_code=True)
V = np.array(0.)
dt = 1.
V_list = []
for t in bp.math.arange(0, 1000, dt):
    V_list.append(V)
    V = step_run1(V,dt)

# bp.integrators.compile_integrators(step_run1,0.,0)
# print(integral.to_math_expr())

plt.plot(V_list)
plt.show()

#------------------- Case 2 ---------------------------------------
# integral = odeint(method="exp_auto", f=derivative2,show_code=True)
# g = np.array(0.)
# dt = 1.
# g_list = []
# for t in bp.math.arange(0, 1000, dt):
#     g_list.append(g)
#     g = step_run2(g,dt)

# bp.integrators.compile_integrators(step_run2,0.)
# print(integral.to_math_expr())


