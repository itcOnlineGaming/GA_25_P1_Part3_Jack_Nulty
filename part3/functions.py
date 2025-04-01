import pandas as pd

def count_unique_players(file_path, user_column="pid"):
    df = pd.read_csv(file_path)
    return df[user_column].nunique()

def calcualte_dau(file_path, date_column="Time", user_column="pid"):
    df = pd.read_csv(file_path, parse_dates=[date_column])
    df["date"] = df[date_column].dt.date
    dau = df.groupby("date")["pid"].nunique().reset_index()
    dau.columns = ["date", "DAU"]
    return dau
    