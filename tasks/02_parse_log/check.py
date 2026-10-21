from solution import parse_log

line = '203.0.113.5 - - [12/Mar/2026:10:11:12 +0000] "GET /api/v1/items?id=3 HTTP/1.1" 200 512\n'
want = {"ip": "203.0.113.5", "method": "GET", "path": "/api/v1/items?id=3", "status": 200, "bytes": 512}
assert parse_log(line) == want, parse_log(line)

line = '10.0.0.1 - - [01/Jan/2026:00:00:00 +0000] "POST /submit HTTP/2" 404 -'
want = {"ip": "10.0.0.1", "method": "POST", "path": "/submit", "status": 404, "bytes": 0}
assert parse_log(line) == want, parse_log(line)

for bad in ["", "not a log line", '1.2.3.4 "GET / HTTP/1.1" 200 5']:
    try:
        parse_log(bad)
    except ValueError:
        pass
    else:
        raise AssertionError(f"no ValueError for {bad!r}")
print("ok")
