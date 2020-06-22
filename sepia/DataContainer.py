#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

class DataContainer(object):
    """
    DataContainer serves to contain all data structures for a single data source (simulation or observation).

    This is constructed as part of SepiaData and generally won't be used directly by a user.

    """

    # Attributes passed to constructor:
    #     x      x values (n, p)
    #     y      y values (n, ell)
    #     t      (optional, not needed for obs data) t values (n, q)
    #     y_ind  (optional, needed if ell == 1) multivariate y indices (ell, )
    # Attributes added by class methods (set manually at your own risk):
    #     K        PCA basis
    #     D        discrepancy basis
    #     y_sd     SD of original y values
    #     y_mean   mean of original y values
    #     y_std    standardized y values
    #     x_trans  rescaled/transformed x values
    #     t_trans  rescaled/transformed t values

    def __init__(self, x, y, t=None, y_ind=None):
        """
        Initializes DataContainer object.

        :param x: GP inputs (the ones known for both sim and obs), shape (n, p)
        :param y: GP outputs, shape (n, ell)
        :param t: optional GP inputs (the ones known only for sim), shape (n, q)
        :param y_ind: optional y indices (needed if ell > 1)
        """
        self.x = x
        self.y = y
        # Parse mandatory inputs (x and y)
        if self.x.shape[0] != self.y.shape[0]:
            raise TypeError('Dimension 0 of x and y must be the same size.')
        # Optional inputs (depending on if sim_only or scalar_out)
        if t is not None and t.shape[0] != self.x.shape[0]:
            raise TypeError('Dimension 0 of x and t must be the same size.')
        if self.y.shape[1] > 1 and y_ind is None:
            raise TypeError('y_ind required when y has multivariate output.')
        if y_ind is not None and self.y.shape[1] != y_ind.shape[0]:
            raise TypeError('Dimension 1 of y must match dimension 0 of y_ind.')
        self.t = t
        self.y_ind = y_ind
        # Basis and transform stuff initialized to None
        self.K = None
        self.D = None
        self.y_sd = None
        self.y_mean = None
        self.y_std = None
        self.x_trans = None
        self.t_trans = None

    # These make sure x/y/t are 2D no matter what
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if x.ndim == 1:
            x = x[:, None]
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        if y.ndim == 1:
            y = y[:, None]
        self.__y = y

    @property
    def t(self):
        return self.__t

    @t.setter
    def t(self, t):
        if t is not None:
            if t.ndim == 1:
                t = t[:, None]
        self.__t = t


