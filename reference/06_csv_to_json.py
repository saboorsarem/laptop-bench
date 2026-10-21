import csv
import io
import re

INT = re.compile(r"-?\d+")
FLOAT = re.compile(r"-?\d+\.\d+")


def convert(value):
    if value is None or value == "":
        return None
    if INT.fullmatch(value):
        return int(value)
    if FLOAT.fullmatch(value):
        return float(value)
    return value


def csv_to_json(text):
    reader = csv.DictReader(io.StringIO(text))
    return [{key: convert(value) for key, value in row.items() if key is not None} for row in reader]
