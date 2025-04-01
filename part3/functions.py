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

def calculate_mau(file_path, date_column="Time", user_column="pid"):
    df = pd.read_csv(file_path, parse_dates=[date_column])
    df["month"] = df[date_column].dt.to_period("M")
    mau = df.groupby("month")[user_column].nunique().reset_index()
    mau.columns = ["month", "MAU"]
    return mau


def calcluate_stickiness(file_path):
    dau = calcualte_dau(file_path)
    mau = calculate_mau(file_path)
    dau["month"] = pd.to_datetime(dau["date"]).dt.to_period("M")

    avg_dau = dau.groupby("month")["DAU"].mean().reset_index()

    stickiness_data = avg_dau.merge(mau, on="month")
    
    stickiness_data["Stickiness"] = stickiness_data["DAU"] / stickiness_data["MAU"]

    return stickiness_data
    