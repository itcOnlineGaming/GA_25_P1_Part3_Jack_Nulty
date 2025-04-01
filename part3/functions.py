import pandas as pd

def count_unique_players(file_path, user_column="pid"):
    df = pd.read_csv(file_path)
    return df[user_column].nunique()