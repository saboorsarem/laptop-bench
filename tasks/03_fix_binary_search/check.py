from solution import binary_search

cases = [
    ([], 1, -1),
    ([1], 1, 0),
    ([1], 2, -1),
    ([1, 2], 3, -1),
    ([1, 2], 0, -1),
    ([1, 2, 3, 4, 5], 5, 4),
    ([1, 2, 3, 4, 5], 1, 0),
    ([2, 2, 2, 2], 2, None),
    (list(range(1000)), 999, 999),
]
for arr, target, want in cases:
    got = binary_search(arr, target)
    if want is None:
        assert got in range(len(arr)) and arr[got] == target, f"{target} in {arr} -> {got}"
    else:
        assert got == want, f"{arr} {target} -> {got}, want {want}"
print("ok")
