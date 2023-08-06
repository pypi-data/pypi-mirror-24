"""This module is a practice in the book <Head First Python>, Example for share the module in PyPI."""
def print_lol(the_list, indent=False, num=0):
    """This function is used for printing array's argument recursive."""
    for inner_list in the_list:
        if isinstance(inner_list, list):
            print_lol(inner_list, indent, num+1)
        else:
            if indent:
                for number in range(num):
                    print("\t", end="")
            print(inner_list)
