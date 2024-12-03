import sys
import pandas as pd
from io import StringIO

def safe_reports(df):
    score_matrix = {}
    for col in df.columns:
        temp_df = df.drop(columns=[col])

        # Calculate minDiff and maxDiff for each row
        min_diff = temp_df.diff(axis=1).abs().min(axis=1)
        max_diff = temp_df.diff(axis=1).abs().max(axis=1)

        # Check for increasing and decreasing conditions
        is_decreasing = temp_df.apply(lambda row: row.dropna().is_monotonic_decreasing, axis=1)
        is_increasing = temp_df.apply(lambda row: row.dropna().is_monotonic_increasing, axis=1)

        # Calculate the score for the current column dropped
        score_matrix[col] = ((min_diff > 0) & (max_diff < 4) & (is_decreasing | is_increasing)).astype(int)

    score = pd.DataFrame(score_matrix)
    has_score = score.max(axis=1)

    return score, has_score, has_score.sum()


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

    print(safe_reports(df))