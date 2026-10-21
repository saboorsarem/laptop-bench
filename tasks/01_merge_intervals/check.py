from solution import merge_intervals

cases = [
    ([], []),
    ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
    ([[1, 2], [2, 3]], [[1, 3]]),
    ([[5, 5]], [[5, 5]]),
    ([[4, 7], [1, 4]], [[1, 7]]),
    ([[1, 10], [2, 3], [4, 5]], [[1, 10]]),
]
for given, want in cases:
    got = merge_intervals([list(pair) for pair in given])
    assert got == want, f"{given} -> {got}, want {want}"

original = [[3, 4], [1, 2]]
merge_intervals(original)
assert original == [[3, 4], [1, 2]], "input was modified"
print("ok")
