
import torch
aa = torch.cuda.is_available()
print(f"torch: {aa}")

import tensorflow as tf
bb = tf.config.list_physical_devices('GPU')
bbb = tf.test.is_gpu_available()
print(f"tensorflow: {bbb}")


import jax
import jax.numpy as jnp
cc = jax.devices()
print(f"jax: {cc}")
