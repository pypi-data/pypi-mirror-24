#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  signature_extractor.py
#
#  Copyright 2017 Bruno S <bruno@oac.unc.edu.ar>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


# =============================================================================
# FUTURE
# =============================================================================

from __future__ import unicode_literals


# =============================================================================
# DOC
# =============================================================================

__doc__ = """"""


# =============================================================================
# IMPORTS
# =============================================================================

import numpy as np

from .core import Extractor


# =============================================================================
# EXTRACTOR CLASS
# =============================================================================

class Signature(Extractor):

    data = ['magnitude', 'time']
    dependencies = ['PeriodLS', 'Amplitude']
    params = {"xbins": 18, "ybins": 12}

    features = []
    for i in range(params["xbins"]):
        for j in range(params["ybins"]):
            features.append("Signature_x_{}_y_{}".format(i, j))

    # this variable stores a sorted version of the features
    # because feets only stores a frozenset of the original features
    # for future validation.
    sorted_features = tuple(features)

    del i, j

    def fit(self, magnitude, time, PeriodLS, Amplitude, xbins, ybins):

        lc_yaxis = (magnitude - np.min(magnitude)) / np.float(Amplitude)

        # SHIFT TO BEGIN AT MINIMUM
        loc = np.argmin(lc_yaxis)
        lc_phase = np.remainder(time - time[loc], PeriodLS) / PeriodLS

        bins = (xbins, ybins)
        counts = np.histogram2d(lc_phase, lc_yaxis, bins=bins, normed=True)[0]

        result = zip(self.sorted_features, counts.reshape(xbins * ybins))

        return dict(result)
