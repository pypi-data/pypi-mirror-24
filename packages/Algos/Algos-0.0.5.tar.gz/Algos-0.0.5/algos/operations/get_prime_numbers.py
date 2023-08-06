"""
    This is the operations module that has all the basic operations specified that will be used frquently in programming
"""
import timeit

class GetPrimeNumbers(object):
    """
	Takes two values and swaps them
        Basic Usage:

	    >>> instance = GetPrimeNumbers(5)
        >>> prime_number_list = instance.sieve_of_eratothenes()
        >>> print prime_number_list
        [2, 3, 5]

    """
    def __init__(self, value1):
        self.value1 = value1 + 1
        self.list = []

    def sieve_of_eratothenes(self):
        prime = [True for i in range(self.value1)]
        p=2
        while (p * p <= self.value1):

            # If prime[p] is not changed, then it is a prime
            if (prime[p] == True):

                # Update all multiples of p
                for i in range(p * 2, self.value1, p):
                    prime[i] = False
            p+=1


        # Print all prime numbers
        for p in range(2, self.value1):
            if prime[p]:
                self.list.append(p)
        return self.list