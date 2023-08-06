# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        ivalutils (package)
## Purpose:     Basic interval arithmetic, sequences of intervals and mappings
#               on intervals
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) 2016 ff. Michael Amrhein
## License:     This program is part of a larger application. For license
##              details please read the file LICENSE.TXT provided together
##              with the application.
##----------------------------------------------------------------------------
## $Source: ivalutils/__init__.py $
## $Revision: fd4faae9086b 2017-09-04 11:00 +0200 michael $


"""Basic interval arithmetic, sequences of intervals and mappings on intervals
"""


# standard library imports
from __future__ import absolute_import

# local imports
from .interval import (
    Limit, LowerLimit, LowerInfiniteLimit, UpperLimit, UpperInfiniteLimit,
    LowerClosedLimit, LowerOpenLimit, UpperClosedLimit, UpperOpenLimit,
    Interval, InvalidInterval, ChainableInterval, ClosedInterval,
    LowerClosedInterval, LowerOpenInterval, OpenBoundedInterval,
    OpenFiniteInterval, UpperClosedInterval, UpperOpenInterval,
)
from .interval_chain import IntervalChain
from .interval_map import IntervalMapping


__version__ = 0, 8, 1


__all__ = [
    'Limit',
    'LowerLimit',
    'LowerInfiniteLimit',
    'UpperLimit',
    'UpperInfiniteLimit',
    'LowerClosedLimit',
    'LowerOpenLimit',
    'UpperClosedLimit',
    'UpperOpenLimit',
    'Interval',
    'InvalidInterval',
    'ClosedInterval',
    'OpenBoundedInterval',
    'OpenFiniteInterval',
    'OpenBoundedInterval',
    'LowerClosedInterval',
    'UpperClosedInterval',
    'LowerOpenInterval',
    'UpperOpenInterval',
    'ChainableInterval',
    'IntervalChain',
    'IntervalMapping',
]
