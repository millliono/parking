import os
import pandas as pd

def save_parking_to_csv(
    hourly_list,
    subscription_list,
    hourly_filename="hourly_parking.csv",
    subscription_filename="subscription_parking.csv",
):
    df_hourly = pd.DataFrame(hourly_list)
    df_subscription = pd.DataFrame(subscription_list)

    df_hourly.to_csv(hourly_filename, index=False)
    df_subscription.to_csv(subscription_filename, index=False)


def initialize_csv(file_path="actions.csv"):
    if os.path.exists(file_path):
        os.remove(file_path)
    headers = ["license", "type", "action", "spot", "timestamp", "pay"]
    df = pd.DataFrame(columns=headers)
    df.to_csv(file_path, mode="w", header=True, index=False)


def log_csv(license, type, action, spot, timestamp, pay):
    new_data = pd.DataFrame(
        [[license, type,  action, spot, timestamp, pay]],
        columns=["license", "type", "action", "spot", "timestamp", "pay"],
    )
    new_data.to_csv("actions.csv", mode="a", header=False, index=False)


initialize_csv()
