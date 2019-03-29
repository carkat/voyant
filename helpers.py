def take(n, lst):
    'if n is positive, take the front, if negative take the back'
    return drop(-n, lst)

def drop(n, lst):
    'if n is positive, drop the front, if negative drop the back'
    return lst[n:] if n > 0 else lst[:-n]

def first(lst):
    'Get the first from a list'
    return lst[0] if len(lst) else None

def rest(lst):
    'Get all but the first of a list'
    return drop(1, lst)
