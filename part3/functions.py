import pandas as pd


# 3.2
def count_unique_players(file_path, user_column="pid"):
    df = pd.read_csv(file_path)
    return df[user_column].nunique()

# 3.3
def calcualte_dau(file_path, date_column="Time", user_column="pid"):
    df = pd.read_csv(file_path, parse_dates=[date_column])
    df["date"] = df[date_column].dt.date
    dau = df.groupby("date")["pid"].nunique().reset_index()
    dau.columns = ["date", "DAU"]
    return dau

# 3.4
def calculate_mau(file_path, date_column="Time", user_column="pid"):
    df = pd.read_csv(file_path, parse_dates=[date_column])
    df["month"] = df[date_column].dt.to_period("M")
    mau = df.groupby("month")[user_column].nunique().reset_index()
    mau.columns = ["month", "MAU"]
    return mau


# 3.5
def calcluate_stickiness(file_path):
    dau = calcualte_dau(file_path)
    mau = calculate_mau(file_path)
    dau["month"] = pd.to_datetime(dau["date"]).dt.to_period("M")

    avg_dau = dau.groupby("month")["DAU"].mean().reset_index()

    stickiness_data = avg_dau.merge(mau, on="month")
    
    stickiness_data["Stickiness"] = stickiness_data["DAU"] / stickiness_data["MAU"]

    return stickiness_data


# 3.6
def calcluate_sessions(start_file, end_file):
    login = pd.read_csv(start_file, parse_dates=["Time"])
    exit = pd.read_csv(end_file, parse_dates=["Time"])
    
    sessions = pd.merge_asof(
        login.sort_values("Time"),
        exit.sort_values("Time"),
        on="Time",
        by="pid",
        suffixes=("_login", "_exit")
    )
    sessions["session_duration"] = (sessions["Time"] - sessions["Time"]).dt.total_seconds() / 60
    return sessions

def calculate_median_session_duration(sessions):
    return sessions["session_duration"].median()

def calculate_sessions_per_user(sessions):
    sessions["month"] = sessions["Time"].dt.to_period("M")
    sessions_per_user = sessions.groupby(["month", "pid"]).size().reset_index(name="sessions_count")
    
    avg_sessions = sessions_per_user.groupby("month")["sessions_count"].mean().reset_index()
    avg_sessions.columns = ["month", "avg_sessions_per_user"]
    return avg_sessions