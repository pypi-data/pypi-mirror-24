"""
    This is the operations module that has all the basic operations specified that will be used frquently in programming
"""

class OddOrEven(object):
    """
	Takes a value and find if it is odd or even
        Basic Usage:

	    >>> instance = OddOrEven(1)
        >>> value1 = instance.get_odd_or_even()
        >>> print value1
        Odd
    """
    def __init__(self, value1):
        self.value1 = value1

    def get_odd_or_even(self):
        status = ''
        if self.value1 % 2 == 0:
            status = 'Even'
        else:
            status = 'Odd'
        return status
