"""
    This is the sorting module that has all the basic operations specified that will be used frquently in programming
"""

class SelectionSort(object):
    """
        Basic Usage:

        Simply Sorting

	    >>> instance = SelectionSort([12, 65, 23, 67, 45, 78, 90, 34, 23, 67, 45])
        >>> sorted_list = instance.sort()
        >>> sorted_list
        [12, 23, 23, 34, 45, 45, 65, 67, 67, 78, 90]

        Sorting in the Reverse Order

        >>> instance = SelectionSort([12, 65, 23, 67, 45, 78, 90, 34, 23, 67, 45])
        >>> sorted_list = instance.sort(reverse=True)
        >>> sorted_list
        [90, 78, 67, 67, 65, 45, 45, 34, 23, 23, 12]
    """
    def __init__(self, *args):
        self.input_list = args[0]

    def sort(self, reverse=False):
        i=0;j=1;temp=0
        for i in range(0, len(self.input_list)):
            j=i
            for j in range(0, len(self.input_list)):
                if reverse==True:
                    if self.input_list[i] > self.input_list[j]:
                        temp = self.input_list[j]
                        self.input_list[j] = self.input_list[i]
                        self.input_list[i] = temp
                else:
                    if self.input_list[i] < self.input_list[j]:
                        temp = self.input_list[i]
                        self.input_list[i] = self.input_list[j]
                        self.input_list[j] = temp

        return self.input_list