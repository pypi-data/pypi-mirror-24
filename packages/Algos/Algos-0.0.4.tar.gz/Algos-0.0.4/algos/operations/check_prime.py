"""
    This is the operations module that has all the basic operations specified that will be used frquently in programming
"""
import timeit

class Prime(object):
    """
	Takes two values and swaps them
        Basic Usage:

	    >>> instance = Prime(2)
        >>> is_prime = instance.check_prime_brute_force()
        >>> print is_prime
        True
        >>> is_prime = instance.check_prime_brute_force_variation()
        >>> print is_prime
        True
    """
    def __init__(self, value1):
        self.value1 = value1

    def check_prime_brute_force(self):
        is_prime = True
        for i in range(2, self.value1):
            if self.value1 % i == 0:
                is_prime = False
                break
        return is_prime

    def check_prime_brute_force_variation(self):
        is_prime = True
        for i in range(2, (self.value1 / 2) + 1):
            if self.value1 % i == 0:
                is_prime = False
                break
        return is_prime