"""Checker for strings to have balanced punctuation.

This module provides functionality to check whether brackets, quotation marks, tags etc. inside the string are balanced,
i.e. whether each o them is opened and closed properly with respect to other punctuation.

The module exports:
    class Balance           Balance checker for strings with given balancing parameters
                            (see help(Balance) for more details).
    function is_unbalanced  Creates Balance object and passes string to its is_unbalanced() method. Takes as parameters
                            the string to check and the parameters for Balance constructor.
"""

from .balance import Balance
__version__ = '0.2.1'


def is_unbalanced(string, pairs=None, symmetrical=None, tags=False, ignore_case=False, cjk=False, straight=False,
                  custom=False, german=False, math=False):
    """Check if the string is balanced and return None or an Unbalanced object."""
    balancer = Balance(pairs, symmetrical, tags, ignore_case, cjk, straight, custom, german, math)
    return balancer.is_unbalanced(string)
