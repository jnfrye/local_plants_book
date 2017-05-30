"""Tests of `scalar.py`"""


from random import uniform, randrange

import PyFloraBook.calculate.scalar as scalar


def test_1_is_normed():
    """The number 1 is trivially normed.
    """
    assert scalar.is_normed(1)


def test_outside_threshold_not_normed():
    """A value outside the threshold from 1 is not normed.
    """
    threshold = .1
    scalar_outside_threshold = \
        1 + uniform(threshold, 5.) * (-1) ** randrange(1)
    assert not scalar.is_normed(scalar_outside_threshold)
