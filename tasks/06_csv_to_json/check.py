from solution import csv_to_json

assert csv_to_json("a,b\n1,2.5\n") == [{"a": 1, "b": 2.5}]
assert csv_to_json("name,score\nalice,3\nbob,\n") == [{"name": "alice", "score": 3}, {"name": "bob", "score": None}]
assert csv_to_json('x,y\n"hello, world",-7') == [{"x": "hello, world", "y": -7}]
assert csv_to_json("a\n1\n2\n") == [{"a": 1}, {"a": 2}]
assert csv_to_json("a,b\n") == []
print("ok")
