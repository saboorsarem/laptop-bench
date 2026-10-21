from solution import chunk

assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
assert chunk([1, 2, 3], 3) == [[1, 2, 3]]
assert chunk([1, 2, 3], 5) == [[1, 2, 3]]
assert chunk([], 3) == []
assert chunk("abcdef", 2) == [["a", "b"], ["c", "d"], ["e", "f"]], chunk("abcdef", 2)
source = [1, 2, 3]
chunk(source, 2)
assert source == [1, 2, 3]
for bad in (0, -1):
    try:
        chunk([1], bad)
    except ValueError:
        pass
    else:
        raise AssertionError(f"no ValueError for n={bad}")
print("ok")
