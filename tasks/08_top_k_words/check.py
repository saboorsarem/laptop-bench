from solution import top_k_words

assert top_k_words("the cat, the dog. The end!", 2) == [("the", 3), ("cat", 1)]
assert top_k_words("a b b c c c", 3) == [("c", 3), ("b", 2), ("a", 1)]
assert top_k_words("", 5) == []
assert top_k_words("one", 0) == []
assert top_k_words("x y", 10) == [("x", 1), ("y", 1)]
assert top_k_words("a_b a", 2) == [("a", 2), ("b", 1)]
print("ok")
