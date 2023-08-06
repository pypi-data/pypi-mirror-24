from fractions import Fraction
from math import gcd
import numpy as np
from time import time
from functools import reduce

class FractMatObj:
    def __init__(self, num, den):
        self.ifnone = lambda a,b: b if a is None else a
        if isinstance(num,list):
            self.num = np.array(num) if isinstance(num[0], list) else np.array(num,np.newaxis)
            self.den = np.array(den) if isinstance(den[0], list) else np.array(den,np.newaxis)
        elif isinstance(num, np.ndarray):
            self.num = num if num.ndim == 2 else num.reshape((1,len(num)))
            self.den = den if den.ndim == 2 else den.reshape((1,len(den)))
        elif isinstance(num, np.int64):
            self.num = np.array([num],dtype=np.int).reshape((1,1))
            self.den = np.array([den],dtype=np.int).reshape((1,1))

        self.shape = self.num.shape

    def __add__(self, other):
        if isinstance(other, FractMatObj):
            if self.shape == other.shape:
                result_num = self.num*other.den+other.num*self.den
                result_den = self.den*other.den
            else:
                raise KeyError("The shapes must be the same")
        elif isinstance(other, int):
            result_num = self.num+other*self.den
            result_den = self.den
        elif isinstance(other, Fraction):
            result_num = self.num*other.denominator+other.numerator*self.den
            result_den = self.den*other.denominator
        else:
            raise NotImplementedError("This function isn't implemented. You can use add fraction, FracMatObj or int")
        gcd_arr = numpy_gcd(result_num, result_den)
        result_num = np.floor_divide(result_num,gcd_arr)
        result_den = np.floor_divide(result_den,gcd_arr)
        return FractMatObj(result_num, result_den)

    def element_wise_mult(self, a, b):
        result_num = a.num * b.num
        result_den = a.den * b.den
        return FractMatObj(result_num, result_den)

    def iter_num_den(self,l):
        for i in range(l.shape[1]):
            yield [l.num[0,i],l.den[0,i]]

    def sum(self, l):
        if l.shape[1] == 1:
            return l[0,0]
        if l.shape[1] % 2 == 0:
            a = l[0,:l.shape[1]//2]
            b = l[0,l.shape[1]//2:]
            l = a+b
            return self.sum(l)
        else:
            l[0,-2] += l[0,-1]
            a = l[0, :l.shape[1] // 2]
            b = l[0, l.shape[1] // 2:-1]
            l = a + b
            return self.sum(l)

    def __neg__(self):
        return FractMatObj(-self.num, self.den)

    def __sub__(self, other):
        return self.__add__(-other)

    def dot(self, other):
        if isinstance(other, FractMatObj):
            if self.shape[1] == other.shape[0] and self.shape[0] == other.shape[1]:
                result_num = np.zeros((self.shape[0], self.shape[0]), dtype=np.int)
                result_den = np.zeros((self.shape[0], self.shape[0]), dtype=np.int)
                # for each row
                for y in range(self.shape[0]):
                    # for each column
                    for x in range(other.shape[1]):
                        elewise_mult = self.element_wise_mult(self[y], other[:, x])
                        sum_val = self.sum(elewise_mult)
                        result_num[y, x] = sum_val.numerator
                        result_den[y, x] = sum_val.denominator
            else:
                if self.shape[1] != other.shape[0]:
                    raise KeyError("Shapes doesn't match %d != %d" % (self.shape[1], other.shape[0]))
                if self.shape[0] != other.shape[1]:
                    raise KeyError("Shapes doesn't match %d != %d" % (self.shape[0], other.shape[1]))
        else:
            raise NotImplementedError("The dot product can only be used with two fracmat objects")
        gcd_arr = numpy_gcd(result_num, result_den)
        result_num = np.floor_divide(result_num, gcd_arr)
        result_den = np.floor_divide(result_den, gcd_arr)
        return FractMatObj(result_num, result_den)

    def __mul__(self, other):
        if isinstance(other, FractMatObj):
            raise NotImplementedError("Maybe you wan't to use .dot()")
        elif isinstance(other, int):
            result_num = self.num*other
            result_den = self.den
        elif isinstance(other, Fraction):
            result_num = self.num*other.numerator
            result_den = self.den*other.denominator
        else:
            raise NotImplementedError("Multiplication can only be used with int and fraction")
        gcd_arr = numpy_gcd(result_num, result_den)
        result_num = np.floor_divide(result_num,gcd_arr)
        result_den = np.floor_divide(result_den,gcd_arr)
        return FractMatObj(result_num, result_den)

    def __div__(self, other):
        return self.divide(other)

    def __truediv__(self, other):
        return self.divide(other)

    def divide(self, other):
        if isinstance(other, int):
            result_num = self.num
            result_den = self.den*other
        elif isinstance(other, Fraction):
            result_num = self.num*other.denominator
            result_den = self.den*other.numerator
        else:
            raise NotImplementedError("Division can only be used with int and fraction")
        gcd_arr = numpy_gcd(result_num, result_den)
        result_num = np.floor_divide(result_num,gcd_arr)
        result_den = np.floor_divide(result_den,gcd_arr)
        return FractMatObj(result_num, result_den)

    def transpose(self):
        return FractMatObj(self.num.T, self.den.T)

    def __getitem__(self, key):
        if isinstance(key, tuple):
            # single entry
            if isinstance(key[0], int) and isinstance(key[1], int):
                return Fraction(self.num[key[0],key[1]],self.den[key[0],key[1]])
            key0_s_o_i = True if isinstance(key[0], slice) or isinstance(key[0], int) else False
            key1_s_o_i = True if isinstance(key[1], slice) or isinstance(key[1], int) else False
            if key0_s_o_i and key1_s_o_i:
                return FractMatObj(self.num[key],self.den[key])
            else:
                raise NotImplementedError()
        else:
            # row
            if isinstance(key, int):
                return FractMatObj(self.num[key],self.den[key])
            else:
                raise NotImplementedError()

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            if isinstance(value, int):
                self.num[key[0],key[1]] = value
                self.den[key[0],key[1]] = 1
            elif isinstance(value, Fraction):
                self.num[key[0],key[1]] = value.numerator
                self.den[key[0],key[1]] = value.denominator
            elif isinstance(value, FractMatObj):
                l_shape = self.num[key].shape if self.num[key].ndim == 2 else (1, self.num[key].shape[0])
                if l_shape == value.num.shape:
                    self.num[key] = value.num
                    self.den[key] = value.den
                else:
                    raise KeyError("Must have the same shape")
            elif isinstance(value, list):
                l_shape = self.num[key].shape if self.num[key].ndim == 2 else (1, self.num[key].shape[0])
                if l_shape[1] == len(value):
                    self.num[key] = [value[x].numerator for x in range(len(value))]
                    self.den[key] = [value[x].denominator for x in range(len(value))]
                else:
                    raise KeyError("Must have the same shape")
            else:
                raise NotImplementedError()
        else:
            if isinstance(value, int):
                self.num[key] = value
                self.den[key] = 1
            elif isinstance(value, Fraction):
                self.num[key] = value.numerator
                self.den[key] = value.denominator
            elif isinstance(value, FractMatObj):
                l_shape = self.num[key].shape if self.num[key].ndim == 2 else (1,self.num[key].shape[0])
                if l_shape == value.num.shape:
                    self.num[key] = value.num
                    self.den[key] = value.den
                else:
                    raise KeyError("Must have the same shape")
            elif isinstance(value, list):
                l_shape = self.num[key].shape if self.num[key].ndim == 2 else (1, self.num[key].shape[0])
                if l_shape[1] == len(value):
                    self.num[key] = [value[x].numerator for x in range(len(value))]
                    self.den[key] = [value[x].denominator for x in range(len(value))]
                else:
                    raise KeyError("Must have the same shape")
            else:
                raise NotImplementedError()

    def __str__(self):
        # compute len for each element
        len_arr = [[0]*self.shape[1] for x in range(self.shape[0])]
        str_arr = [[""]*self.shape[1] for x in range(self.shape[0])]
        # str_arr =
        for y in range(self.shape[0]):
            for x in range(self.shape[1]):
                n_val = self.num[y,x]
                d_val = self.den[y,x]
                frac = n_val/d_val
                if int(frac) == frac:
                    len_arr[y][x] = len(" %d" % frac)
                    str_arr[y][x] = " %d" % frac
                else:
                    len_arr[y][x] = len(" %d/%d" % (n_val,d_val))
                    str_arr[y][x] = " %d/%d" % (n_val,d_val)

        str_arr_col = list(zip(*str_arr))
        i = 0
        for col in zip(*len_arr):
            max_val = max(col)+2
            str_arr_col[i] = [" "*(max_val-len(x))+str(x) for x in str_arr_col[i]]
            i += 1

        str_arr = list(zip(*str_arr_col))
        output = ""
        for row in str_arr:
            line = "["
            for ele in row:
                line +=  ele
            output += line+"]\n"

        return output[:-1]

def numpy_gcd(a, b):
    shape = a.shape
    a = a.copy().flatten()
    b = b.copy().flatten()
    pos = np.nonzero(b)[0]
    while len(pos) > 0:
        b2 = b[pos]
        a[pos], b[pos] = b2, a[pos] % b2
        pos = pos[b[pos] != 0]
    return a.reshape(shape)