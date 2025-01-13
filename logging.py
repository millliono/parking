import pandas as pd


def _log_entry(log_file, type, car_license, driver_name, spot, start, end, charge=0):
    # Append a log entry to the in-memory log
    def _save_log(data):
        # Save the log data to the file using pandas
        df = pd.DataFrame(data)
        df.to_csv(log_file, index=False, mode='a', header=False)
    
    data = {
        "Type": [type],
        "Car License": [car_license],
        "Driver_name": [driver_name],
        "Spot": [spot],
        "Start":[start],
        "End": [end],
        "Charge": [charge]
    }
    _save_log(data)  # Save the log data to the file

