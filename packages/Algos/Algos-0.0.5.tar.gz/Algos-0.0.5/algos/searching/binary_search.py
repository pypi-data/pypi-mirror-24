"""
    This is the searching module that has all the searching operations that will be used frequently in programming
"""

class BinarySearch(object):
    """
	Takes two values and swaps them
        Basic Usage:
	    >>> instance = BinarySearch(56, [12,34,23,56,45,67])
        >>> element = instance.search_item_iterative()
        >>> print element
        3

        >>> instance = BinarySearch(56, [12,34,23,56,45,67])
        >>> element = instance.search_item_recursive()
        >>> print element
        3
    """
    def __init__(self, search, *args):
        self.search = search
        self.input_list = args[0]


    def search_item_iterative(self):
        l = 0
        r = len(self.input_list)
        while l <= r:
            mid = l + (r - l)/2
            # Check if x is present at mid
            if self.input_list[mid] == self.search:
                return mid

            # If x is greater, ignore left half
            elif self.input_list[mid] < self.search:
                l = mid + 1

            # If x is smaller, ignore right half
            else:
                r = mid - 1

        # If we reach here, then the element was not present
        return -1

    def binary_search(self, array, left, right, to_search):
        # Check base case
        if right >= left:

            mid = left + (right - left)/2

            # If element is present at the middle itself
            if array[mid] == to_search:
                return mid

            # If element is smaller than mid, then it can only
            # be present in left subarray
            elif array[mid] > to_search:
                return self.binary_search(array, left, mid-1, to_search)

            # Else the element can only be present in right subarray
            else:
                return self.binary_search(array, mid+1, right, to_search)

        else:
            # Element is not present in the array
            return -1

    def search_item_recursive(self):
        left = 0
        right = len(self.input_list)
        return self.binary_search(self.input_list, left, right, self.search)