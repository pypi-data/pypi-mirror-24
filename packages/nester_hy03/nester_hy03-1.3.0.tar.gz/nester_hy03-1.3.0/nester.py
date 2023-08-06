"""This module is a practice in the book <Head First Python>, Example for share the module in PyPI."""
def print_lol(the_list, num):
    """This function is used for printing array's argument recursive."""
    for inner_list in the_list:
        if isinstance(inner_list, list):
            print_lol(inner_list, num+1)
        else:
            for number in range(num):
                print("\t", end="")
            print(inner_list)
