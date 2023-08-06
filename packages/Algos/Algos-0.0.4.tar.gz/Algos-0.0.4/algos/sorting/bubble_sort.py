"""
    This is the sorting module that has all the basic operations specified that will be used frquently in programming
"""

class BubbleSort(object):
    """
        Basic Usage:

        Simply Sorting

	    >>> instance = BubbleSort([12, 65, 23, 67, 45, 78, 90, 34, 23, 67, 45])
        >>> sorted_list = instance.sort()
        >>> sorted_list
        [12, 23, 23, 34, 45, 45, 65, 67, 67, 78, 90]

        Sorting in the Reverse Order

        >>> instance = BubbleSort([12, 65, 23, 67, 45, 78, 90, 34, 23, 67, 45])
        >>> sorted_list = instance.sort(reverse=True)
        >>> sorted_list
        [90, 78, 67, 67, 65, 45, 45, 34, 23, 23, 12]
    """
    def __init__(self, *args):
        self.input_list = args[0]

    def sort(self, reverse=False):
        for current_number in range(len(self.input_list)-1,0,-1):
            for i in range(current_number):
                if (self.input_list[i] > self.input_list[i+1]) and reverse==False:
                    temp = self.input_list[i]
                    self.input_list[i] = self.input_list[i+1]
                    self.input_list[i+1] = temp
                elif (self.input_list[i] < self.input_list[i+1]) and reverse==True:
                    temp = self.input_list[i]
                    self.input_list[i] = self.input_list[i+1]
                    self.input_list[i+1] = temp
        return self.input_list

