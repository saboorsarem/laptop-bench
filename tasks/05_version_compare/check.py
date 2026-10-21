from solution import version_compare

cases = [
    ("1.2", "1.10", -1),
    ("1.10", "1.2", 1),
    ("1.2.0", "1.2", 0),
    ("2", "1.9.9", 1),
    ("0.0.1", "0.0.1", 0),
    ("10.0", "9.99.99", 1),
    ("1.0.0.1", "1.0.0", 1),
]
for a, b, want in cases:
    got = version_compare(a, b)
    assert got == want, f"({a}, {b}) -> {got}, want {want}"
    assert version_compare(b, a) == -want, f"reverse of ({a}, {b}) -> {version_compare(b, a)}"
print("ok")
