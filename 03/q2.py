import sys
import re
import pandas as pd
from io import StringIO

def main(df):
    multi = df["x"] * df["y"]
    return df, multi, multi.sum()

operation_pattern = r"(\A|do\(\)|don't\(\))"
pattern = r"mul\((?:(\d{1,3}),(\d{1,3}))?\)"

def parse(input_lines):
    total_match  = pd.DataFrame(columns=["x", "y"])
    for operation, text in parse_operations(input_lines):
        if operation != "don't()":
            matches = pd.DataFrame(pd.Series(text.splitlines()).str.extractall(pattern)[[0, 1]].values, columns=["x", "y"])
            total_match = pd.concat([total_match, matches.astype(int)], ignore_index=True)

    return total_match

def parse_operations(text):
    matches = re.split(operation_pattern, text)
    matches.pop(0)
    result = []
    for i in range(0, len(matches), 2):
        result.append(matches[i:i+2])
    return result


if __name__ == "__main__":
    # Use StringIO to treat the string as a file
    txt = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

    if len(sys.argv) > 1:
        txt = open(sys.argv[1], "r").read()


    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print(main(parse(txt)))
    else:
        print(main(parse(txt))[2])
