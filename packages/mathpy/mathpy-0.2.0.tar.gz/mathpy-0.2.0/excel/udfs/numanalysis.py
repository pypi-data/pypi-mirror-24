#encoding=utf8

"""

NUMERICAL ANALYSIS

"""

from mathpy.numerical import polynomial
import xlwings as xw


@xw.func
@xw.arg('x', doc='Array of x-values. Must equal y in length')
@xw.arg('y', doc='Array of y-values. Must equal x in length')
def LAGRANGE_INTERPOLATION(x, y):

    return str(polynomial.lagrange_interpolate(x, y))


@xw.func
@xw.arg('x', doc='Array of x-values. Must equal y in length')
@xw.arg('y', doc='Array of y-values. Must equal x in length')
@xw.arg('x0', doc='Desired value at which to interpolate and approximate poynomial')
@xw.ret(expand='table')
def NEVILLE_INTERPOLATION(x, y, x0):

    return polynomial.neville(x, y, x0)


@xw.func
@xw.arg('x', doc='Array of x-values. Must equal y in length')
@xw.arg('y', doc='Array of y-values. Must equal x in length')
@xw.arg('x0', doc='Desired value at which to interpolate and approximate poynomial')
@xw.ret(expand='table')
def DIVIDED_DIFFERENCES_INTERPOLATION(x, y, x0):

    return polynomial.divided_differences(x, y, x0)