def version_compare(a, b):
    left = [int(part) for part in a.split(".")]
    right = [int(part) for part in b.split(".")]
    width = max(len(left), len(right))
    left += [0] * (width - len(left))
    right += [0] * (width - len(right))
    return (left > right) - (left < right)
