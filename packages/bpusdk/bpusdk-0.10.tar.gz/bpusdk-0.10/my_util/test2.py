
from unittest import TestCase

import numpy as np
import pytest
from scipy.sparse import csr_matrix

import brainpy as bp

class TestMatConn(TestCase):
  def test_MatConn1(self):
    bp.math.random.seed(123)
    actual_mat = np.random.randint(2, size=(5, 3), dtype=bp.math.bool_)
    conn = bp.connect.MatConn(conn_mat=actual_mat)(pre_size=5, post_size=3)

    pre2post, post2pre, conn_mat = conn.requires('pre2post', 'post2pre', 'conn_mat')

    print()
    print('conn_mat', conn_mat)

    assert bp.math.array_equal(conn_mat, actual_mat)

  def test_MatConn2(self):
    conn = bp.connect.MatConn(conn_mat=np.random.randint(2, size=(5, 3), dtype=bp.math.bool_))
    with pytest.raises(AssertionError):
      conn(pre_size=5, post_size=1)

bp.math.random.seed(123)
actual_mat = np.random.randint(2, size=(5, 3), dtype=bp.math.bool_)
conn = bp.connect.MatConn(conn_mat=actual_mat)(pre_size=5, post_size=3)

pre2post, post2pre, conn_mat = conn.requires('pre2post', 'post2pre', 'conn_mat')

print()
print('conn_mat', conn_mat)
print('actual_mat', conn_mat)