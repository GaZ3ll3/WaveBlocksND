"""The WaveBlocks Project

This file contains the class for (generalized) Gauss-Laguerre quadrature.

@author: R. Bourquin
@copyright: Copyright (C) 2013 R. Bourquin
@license: Modified BSD License
"""

from copy import deepcopy
from numpy import zeros, floating, real
from scipy import pi, exp, sqrt
from scipy.special.orthogonal import la_roots

from QuadratureRule import QuadratureRule

__all__ = ["GaussHermiteQR"]


class GaussLaguerreQR(QuadratureRule):
    r"""This class implements a (generalized) Gauss-Laguerre quadrature rule.
    """

    def __init__(self, order, a=0, options={}):
        r"""Initialize a new quadrature rule.

        :param order: The order :math:`R` of the Gauss-Laguerre quadrature.
        :param a: The parameter :math:`a > -1` of the generalized Gauss-Laguerre quadrature.
                  This value defaults to `0` resulting in classical Gauss-Laguerre quadrature.

        :raise: :py:class:`ValueError` if order ``order`` is not 1 or above.
        """
        # The space dimension of the quadrature rule.
        self._dimension = 1

        # The order R of the Gauss-Laguerre quadrature.
        self._order = order
        self._a = a

        # Qudrature has to have at least a single (node,weight) pair.
        if not self._order > 0:
            raise ValueError("Quadrature rule has to be of order 1 at least.")

        # Set the options
        self._options = options

        nodes, weights = la_roots(self._order, self._a)

        # The number of nodes in this quadrature rule
        self._number_nodes = nodes.size

        # Transform quadrature weights
        h = self._hermite_recursion(real(sqrt(nodes)))
        weights = (sqrt(2.0*order-1.0) / (sqrt(2.0)*(order**2-order/2.0))
                   * sqrt(nodes) / (h[2*order-2,:] * h[2*order-1,:]))

        # The quadrature nodes \gamma.
        self._nodes = real(nodes).reshape((1,self._number_nodes))
        # The quadrature weights \omega.
        self._weights = real(weights).reshape((1,self._number_nodes))


    def __str__(self):
        return "Gauss-Laguerre quadrature rule of order " + str(self._order) + " with a=" + str(self._a)


    def get_description(self):
        r"""Return a description of this quadrature rule object.
        A description is a ``dict`` containing all key-value pairs
        necessary to reconstruct the current instance. A description
        never contains any data.
        """
        d = {}
        d["type"] = "GaussLaguerreQR"
        d["dimension"] = self._dimension
        d["order"] = self._order
        d["a"] = self._a
        d["options"] = deepcopy(self._options)
        return d


    def get_nodes(self):
        r"""Returns the quadrature nodes :math:`\gamma_i`.

        :return: An array containing the quadrature nodes :math:`\gamma_i`.
        """
        return self._nodes.copy()


    def get_weights(self):
        r"""Returns the quadrature weights :math:`\omega_i`.

        :return: An array containing the quadrature weights :math:`\omega_i`.
        """
        return self._weights.copy()


    def _hermite_recursion(self, nodes):
        r"""Evaluate the Hermite functions recursively up to the order :math:`2R - 1` on the given nodes.

        :param nodes: The points at which the Hermite functions are evaluated.
        :return: Returns a twodimensional array :math:`H` where the entry :math:`H[k,i]` is the value
                 of the :math:`k`-th Hermite function evaluated at the node :math:`\gamma_i`.
        """
        H = zeros((2*self._order, nodes.size), dtype=floating)

        H[0] = pi**(-0.25) * exp(-0.5*nodes**2)

        if self._order > 1:
            H[1] = sqrt(2.0) * nodes * H[0]

            for k in xrange(2, 2*self._order):
                H[k] = sqrt(2.0/k) * nodes * H[k-1] - sqrt((k-1.0)/k) * H[k-2]

        return H
