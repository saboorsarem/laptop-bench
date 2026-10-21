from solution import dedupe_keep_order

assert dedupe_keep_order([3, 1, 3, 2, 1]) == [3, 1, 2]
assert dedupe_keep_order([]) == []
assert dedupe_keep_order("banana") == ["b", "a", "n"]
assert dedupe_keep_order([(1, 2), (1, 2), (3,)]) == [(1, 2), (3,)]
source = [1, 1, 2]
result = dedupe_keep_order(source)
assert source == [1, 1, 2], "input was modified"
assert result is not source
print("ok")
