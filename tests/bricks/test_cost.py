import numpy
from numpy.testing import assert_allclose

import theano
from theano import tensor
from theano import function

from blocks.bricks import Softmax
from blocks.bricks.cost import CategoricalCrossEntropy


def test_softmax_vector():
    x = tensor.matrix('x')
    y = tensor.lvector('y')

    softmax_out = Softmax().apply(x)
    cost = CategoricalCrossEntropy().apply(y, softmax_out)

    cost_stable = Softmax().categorical_cross_entropy(y, x)

    softmax_cost_func = function([x, y], cost)
    softmax_cost_stable_func = function([x, y], cost_stable)

    batch_size = 100
    x_size = 10

    rng = numpy.random.RandomState(1)
    x_val = rng.randn(batch_size, x_size).astype(theano.config.floatX)
    y_val = rng.randint(low=0, high=x_size, size=(batch_size))
    softmax_cost = softmax_cost_func(x_val, y_val)
    softmax_cost_stable = softmax_cost_stable_func(x_val, y_val)

    assert_allclose(softmax_cost, softmax_cost_stable)


def test_softmax_matrix():
    x = tensor.matrix('x')
    y = tensor.matrix('y')

    softmax_out = Softmax().apply(x)
    cost = CategoricalCrossEntropy().apply(y, softmax_out)

    cost_stable = Softmax().categorical_cross_entropy(y, x)

    softmax_cost_func = function([x, y], cost)
    softmax_cost_stable_func = function([x, y], cost_stable)

    batch_size = 2
    x_size = 2

    rng = numpy.random.RandomState(1)
    x_val = rng.randn(batch_size, x_size).astype(theano.config.floatX)
    y_val_us = rng.uniform(size=(batch_size,
                                 x_size)).astype(theano.config.floatX)
    y_val = y_val_us / numpy.expand_dims(y_val_us.sum(axis=1), axis=1)
    softmax_cost = softmax_cost_func(x_val, y_val)
    softmax_cost_stable = softmax_cost_stable_func(x_val, y_val)

    assert_allclose(softmax_cost, softmax_cost_stable)
