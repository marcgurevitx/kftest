
def integer_if_possible(x):
    """
    Return integer if number doesn't have decimal part
    """
    i = int(x)
    if i == x:
        return i
    else:
        return x
