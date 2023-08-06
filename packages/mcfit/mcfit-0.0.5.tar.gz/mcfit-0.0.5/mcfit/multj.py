from __future__ import print_function, division
from numpy import pi, abs, ceil, exp, log, log2, angle, \
                array, arange, zeros, concatenate, searchsorted, allclose
from numpy.fft import rfft, hfft


class multj(object):
    r"""Compute integrals with multiple spherical Bessel functions

    .. math:: G(y_1, ..., y_m) = \int_0^\infty
        F(x) \prod_{n_i=1}^m j_{n_i}(xy_i) \,\frac{\mathrm{d}x}x

    by expanding the product of :math:`j_n` in sines and cosines [1]_.

    Parameters
    ----------
    ells : int, array_like
    q : float
        "top-level" power-law tilt

    Attributes
    ----------

    Methods
    -------

    Examples
    --------

    References
    ----------
    .. [1] Our paper
    """
    def __init__(self, x, ells, q, N=None, lowring=True):
    def _setup(self, N):
    def __call__(self, F, y, extrap=True):
        """Evaluate the integral

        Parameters
        ----------
        y : float, array_like
            output arguments, a list of :math:`y_i` arrays. If only one array
            is provided it will be used for each argument

        Returns
        -------
        G : float, array_like
            output function as an :math:`n`-dimensional array
        """
