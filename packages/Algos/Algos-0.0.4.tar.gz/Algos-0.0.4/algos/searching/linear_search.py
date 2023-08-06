"""
    This is the operations module that has all the searching operations that will be used frequently in programming
"""

class LinearSearch(object):
    """
	Takes two values and swaps them
        Basic Usage:
	    >>> instance = LinearSearch([12,34,23,56,45,67])
        >>> item_index = instance.search_item(23)
        >>> print item_index
        2
    """
    def __init__(self, *args):
        self.input_list = args[0]

    def search_item(self, key):
        found = []
        for index, item in enumerate(self.input_list):
            if key == item:
                found.append(index)
        if len(found) == 0:
            return None
        elif len(found) > 1:
            return found
        return found[0]
