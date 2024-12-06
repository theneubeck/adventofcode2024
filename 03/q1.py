import sys
import pandas as pd
from io import StringIO

def main(df):
    multi = df["x"] * df["y"]
    return multi, multi.sum()

pattern = r"mul\((?:(\d{1,3}),(\d{1,3}))?\)"

def parse(text):
    matches = pd.DataFrame(pd.Series(text.splitlines()).str.extractall(pattern)[[0, 1]].values, columns=["x", "y"])
    # Convert to numeric
    matches = matches.astype(int)
    return matches


if __name__ == "__main__":
    # Use StringIO to treat the string as a file
    txt = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

    if len(sys.argv) > 1:
        txt = open(sys.argv[1], "r").read()


    print(main(parse(txt)))
