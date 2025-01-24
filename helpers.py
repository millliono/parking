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
