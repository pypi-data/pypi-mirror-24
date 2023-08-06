

"""

SET THEORY

"""


from mathpy.settheory.sets import Set, iselement, issubset
import xlwings as xw
import numpy as np


@xw.func
@xw.arg('a', np.array, doc='First set')
@xw.arg('b', np.array, doc='Second set')
@xw.ret(expand='table')
def UNION(a, b):
    r"""
    Performs the set union operation of two sets.

    Parameters
    ----------
    a
        Continuous range of cells composing first set.
    b
        Continuous range of cells composing second set.

    See Also
    --------
    nunion : function
        Function that performs set union operation. Function accepts n number of
        sets.

    Returns
    -------
    array-like
        Continuous range of cells comprising union of two sets

    """
    return Set.nunion(a, b)


@xw.func
@xw.arg('a', np.array, doc='First set')
@xw.arg('b', np.array, doc='Second set')
@xw.ret(expand='table')
def INTERSECT(a, b):
    r"""
    Performs the intersection of two sets.

    Parameters
    ----------
    a
        Continuous range of cells composing first set.
    b
        Continuous range of cells composing second set.

    See Also
    --------
    nintersect : function
        Function used to perform the set intersection operation. Unlike the Excel UDF,
        the nintersect function can accept any number of sets.

    Returns
    -------
    Continuous range comprising the set resulting from the set intersection operation.

    """
    return Set.nintersect(a, b)


@xw.func
@xw.arg('a', np.array, doc='First set')
@xw.arg('b', np.array, doc='Second set')
def RELATIVECOMP(a, b):
    """
    Performs the relative complement of two sets.

    Parameters
    ----------
    a
        Continuous range of cells composing first set.
    b
        Continuous range of cells composing second set.

    See Also
    --------
    ndifference : function
        Function used to compute the relative complement of two sets.

    Returns
    -------
    Continuous range comprising the set resulting from the relative complement operation.

    """
    return Set.ndifference(a, b)


@xw.func
@xw.arg('a', np.array, doc='First set')
@xw.arg('b', np.array, doc='Second set')
def ISEQUALSET(a, b):
    """


    Parameters
    ----------
    a
    b

    Returns
    -------

    """
    return Set.isequalset(a, b)


@xw.func
@xw.arg('x', doc='Element to test for set membership')
@xw.arg('a', np.array, doc='Set desired to test')
def ISELEMENT(x, a):

    return iselement(x, a)


@xw.func
@xw.arg('a', np.array, doc='First set to test')
@xw.arg('b', np.array, doc='Second set to test for existence of subset')
def ISSUBSET(a, b):

    return issubset(a, b)