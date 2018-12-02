def custom_min(a, b):
    if a is None:
        return b
    elif b is None:
        return a
    return min(a, b)


def custom_max(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return max(a, b)
