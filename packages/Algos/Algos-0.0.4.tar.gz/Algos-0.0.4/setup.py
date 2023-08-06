from distutils.core import setup

modules = [
    #'algos.structures',
    'algos.operations.swap',
    'algos.operations.check_prime',
    'algos.operations.odd_or_even',
    'algos.operations.get_prime_numbers',
    'algos.sorting.insertion_sort',
    'algos.sorting.bubble_sort',
    'algos.sorting.selection_sort',
    'algos.searching.linear_search',
]


setup(
    name         = 'Algos',
    version      = '0.0.4',
    py_modules   =  modules,
    author       = 'Chitrank Dixit',
    author_email = 'chitrankdixit@gmail.com',
    url          = 'http://chitrank-dixit.github.io',
    description  = 'A simple library that consists of all basic operations and complex algorithm present on the globe' 

)
