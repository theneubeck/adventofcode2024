import sys
import pandas as pd
from io import StringIO

def safe_reports(df):
    minDiff = df.apply(lambda row: row.diff().dropna().abs().min(), axis=1)
    maxDiff = df.apply(lambda row: row.diff().dropna().abs().max(), axis=1)

    decreasing = df.apply(lambda row: row.dropna().is_monotonic_decreasing, axis=1)
    increasing = df.apply(lambda row: row.dropna().is_monotonic_increasing, axis=1)

    df["minDiff"] = minDiff
    df["maxDiff"] = maxDiff
    df["decreasing"] = decreasing
    df["increasing"] = increasing

    score = ((df["minDiff"] > 0) & (df["maxDiff"] < 4) & (df["decreasing"] | df["increasing"])).astype(int)

    return df, score, score.sum()


if __name__ == "__main__":
    # Use StringIO to treat the string as a file
    txt = """
    7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9
    """
    data = StringIO(txt)

    if len(sys.argv) > 1:
        data = open(sys.argv[1], "r")

    # Read the data into a DataFrame
    df = pd.read_csv(data, sep=r'\s+', header=None)

    print(safe_reports(df)[2])