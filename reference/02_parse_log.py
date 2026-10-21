import re

PATTERN = re.compile(r'^(\S+) \S+ \S+ \[[^\]]+\] "([A-Z]+) (\S+) [^"]*" (\d{3}) (\d+|-)$')


def parse_log(line):
    match = PATTERN.match(line.rstrip("\n"))
    if not match:
        raise ValueError(f"not an access log line: {line!r}")
    ip, method, path, status, size = match.groups()
    return {
        "ip": ip,
        "method": method,
        "path": path,
        "status": int(status),
        "bytes": 0 if size == "-" else int(size),
    }
