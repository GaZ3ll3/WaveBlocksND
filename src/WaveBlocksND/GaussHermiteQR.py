"""The WaveBlocks Project

This file contains the class for Gauss-Hermite quadrature.

@author: R. Bourquin
@copyright: Copyright (C) 2010, 2011, 2012, 2013 R. Bourquin
@license: Modified BSD License
"""

from copy import deepcopy
from numpy import zeros, floating, real
from scipy import pi, exp, sqrt
from scipy.special.orthogonal import h_roots

from QuadratureRule import QuadratureRule

__all__ = ["GaussHermiteQR"]


class GaussHermiteQR(QuadratureRule):
    r"""This class implements a Gauss-Hermite quadrature rule.
    """

    def __init__(self, order, options={}):
        r"""Initialize a new quadrature rule.

        :param order: The order :math:`k` of the Gauss-Hermite quadrature.
                      From theory we know that a Gauss quadrature rule
                      of order :math:`k` is exact for polynomials up to
                      degree :math:`2 k - 1`.

        :raise: :py:class:`ValueError` if the ``order`` is not 1 or above.
        """
        # The space dimension of the quadrature rule.
        self._dimension = 1

        # The order of the Gauss-Hermite quadrature.
        self._order = order

        # Quadrature has to have at least a single (node,weight) pair.
        if not self._order > 0:
            raise ValueError("Quadrature rule has to be of order 1 at least.")

        # Set the options
        self._options = options

        nodes, weights = h_roots(self._order)

        # The number of nodes in this quadrature rule
        self._number_nodes = nodes.size

        # We deal with real values only, but the array we get from h_roots is of complex dtype
        h = self._hermite_recursion(real(nodes))[-1,:]
        weights = 1.0/((h**2) * self._order)

        # The quadrature nodes \gamma.
        self._nodes = nodes.reshape((1,self._number_nodes))
        # The quadrature weights \omega.
        self._weights = weights
        self._weights = self._weights.reshape((1,self._number_nodes))


    def __str__(self):
        return "Gauss-Hermite quadrature rule of order " + str(self._order)


    def get_description(self):
        r"""Return a description of this quadrature rule object.
        A description is a ``dict`` containing all key-value pairs
        necessary to reconstruct the current instance. A description
        never contains any data.
        """
        d = {}
        d["type"] = "GaussHermiteQR"
        d["dimension"] = self._dimension
        d["order"] = self._order
        d["options"] = deepcopy(self._options)
        return d


    def get_nodes(self):
        r"""Returns the quadrature nodes :math:`\{\gamma_i\}_i`.

        :return: An array containing the quadrature nodes :math:`\{\gamma_i\}_i`.
        """
        return self._nodes.copy()


    def get_weights(self):
        r"""Returns the quadrature weights :math:`\{\omega_i\}_i`.

        :return: An array containing the quadrature weights :math:`\{\omega_i\}_i`.
        """
        return self._weights.copy()


    def _hermite_recursion(self, nodes):
        r"""Evaluate the Hermite functions recursively up to the order :math:`R` on the given nodes.

        :param nodes: The points at which the Hermite functions are evaluated.
        :return: A two dimensional array :math:`H` where the entry :math:`H[k,i]` is the value
                 of the :math:`k`-th Hermite function evaluated at the node :math:`\{\gamma_i\}_i`.
        """
        H = zeros((self._order, nodes.size), dtype=floating)

        H[0] = pi**(-0.25) * exp(-0.5*nodes**2)

        if self._order > 1:
            H[1] = sqrt(2.0) * nodes * H[0]

            for k in xrange(2, self._order):
                H[k] = sqrt(2.0/k) * nodes * H[k-1] - sqrt((k-1.0)/k) * H[k-2]

        return H
