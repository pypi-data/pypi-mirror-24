from ..synthetic import gen_image
from numpy.testing import assert_array_equal
import numpy as np 


def test_gen_image():
    """Test for image_weight"""
    # Swiss
    true_res = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                         [0., 0., 0., 1., 1., 1., 1., 0., 0., 0.],
                         [0., 0., 0., 1., 1., 1., 1., 0., 0., 0.],
                         [0., 1., 1., 1., 1., 1., 1., 1., 1., 0.],
                         [0., 1., 1., 1., 1., 1., 1., 1., 1., 0.],
                         [0., 1., 1., 1., 1., 1., 1., 1., 1., 0.],
                         [0., 1., 1., 1., 1., 1., 1., 1., 1., 0.],
                         [0., 0., 0., 1., 1., 1., 1., 0., 0., 0.],
                         [0., 0., 0., 1., 1., 1., 1., 0., 0., 0.],
                         [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])
    res = gen_image(region='swiss', image_height=10, image_width=10, weight_value=1)
    assert_array_equal(true_res, res)

    # Rectangle
    true_res = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                         [0., 0., 0., 1., 1., 1., 1., 0., 0., 0.],
                         [0., 0., 0., 1., 1., 1., 1., 0., 0., 0.],
                         [0., 0., 0., 1., 1., 1., 1., 0., 0., 0.],
                         [0., 0., 0., 1., 1., 1., 1., 0., 0., 0.],
                         [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                         [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])
    res = gen_image(region='rectangle', image_height=10, image_width=10, weight_value=1)
    assert_array_equal(true_res, res)

    # circle: approximate test
    res = gen_image(region='circle', image_height=60, image_width=60, weight_value=1)
    radius = 20
    surface = np.pi*radius**2
    tol = surface * 0.005  # tolerate 0.5% error
    assert(abs(np.sum(res) - surface) < tol)
