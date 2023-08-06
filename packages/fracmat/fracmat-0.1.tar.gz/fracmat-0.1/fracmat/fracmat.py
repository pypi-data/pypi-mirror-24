from .fracmatObj import FractMatObj
import numpy as np


def array(shape):
    return zeros(shape)


def zeros(shape):
    num = np.zeros(shape, dtype=np.int)
    den = np.ones(shape, dtype=np.int)
    return FractMatObj(num,den)


def ones(shape):
    num = np.ones(shape, dtype=np.int)
    den = np.ones(shape, dtype=np.int)
    return FractMatObj(num, den)
