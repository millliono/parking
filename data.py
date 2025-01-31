import helpers


class Vehicle:
    def __init__(
        self, license, spot=None, driver_name=None, is_sub=False, datetime=None
    ):
        self.license = license
        self.spot = spot
        self.driver_name = driver_name
        self.is_sub = is_sub
        self.datetime = datetime

    def __eq__(self, other):
        if isinstance(other, Vehicle):
            return self.license == other.license
        return False

    def __repr__(self):
        return f"Vehicle(license='{self.license}')"


class ParkingSpace:
    def __init__(self):
        # Initialize a parking space with all spots empty
        self.hourly = [False] * 15  # False means empty
        self.subscription = [{"occupied": False, "vehicle": False} for _ in range(5)]
        self.profit = {}

    def park(self, license, datetime):
        reg = self.find_registered(license)
        if reg is not False:
            self.subscription[reg]["occupied"] = True
            self.subscription[reg]["vehicle"].datetime = datetime
            helpers.log_csv(
                self.subscription[reg]["vehicle"].license,
                "Monthly",
                "Parked",
                self.subscription[reg]["vehicle"].spot,
                self.subscription[reg]["vehicle"].datetime.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                f"${0.0}",
            )
        else:
            # Park a car in the first available spot
            vec = Vehicle(license)
            for index, spot in enumerate(self.hourly):
                if not spot:  # Check if the spot is available (empty)
                    self.hourly[index] = vec
                    vec.spot = index
                    vec.datetime = datetime
                    helpers.log_csv(
                        vec.license,
                        "Hourly",
                        "Parked",
                        vec.spot,
                        vec.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                        f"${0.0}",
                    )
                    return
            print("No available spots.")

    def find_registered(self, license):
        for index, item in enumerate(self.subscription):
            vehicle = item["vehicle"]
            if vehicle and vehicle.license == license:
                return index
        return False

    def rent_spot(self, vehicle, duration):
        if vehicle.spot >= 0 and self.subscription[vehicle.spot]["vehicle"] == False:
            self.subscription[vehicle.spot]["vehicle"] = vehicle
            date_key = vehicle.datetime.date().isoformat()
            self.profit[date_key] = self.profit.get(date_key, 0) + 50 * duration
            helpers.log_csv(
                vehicle.license,
                "Monthly",
                "Rented",
                vehicle.spot,
                vehicle.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                f"${self.profit[date_key]:.2f}",
            )
            return True
        return False

    def remove_car(self, spot, spot_type, datetime):
        time = 0
        if spot_type == "subscription":
            time = datetime - self.subscription[spot]["vehicle"].datetime
            self.subscription[spot]["occupied"] = False
            helpers.log_csv(
                self.subscription[spot]["vehicle"].license,
                "Monthly",
                "Pulled-out",
                self.subscription[spot]["vehicle"].spot,
                self.subscription[spot]["vehicle"].datetime.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                f"${0.0}",
            )
        elif spot_type == "hourly":
            time = datetime - self.hourly[spot].datetime
            date_key = datetime.date().isoformat()
            current_profit = self.calc_profit(time.total_seconds())
            self.profit[date_key] = self.profit.get(date_key, 0) + current_profit
            helpers.log_csv(
                self.hourly[spot].license,
                "Hourly",
                "Pulled-Out",
                self.hourly[spot].spot,
                self.hourly[spot].datetime.strftime("%Y-%m-%d %H:%M:%S"),
                f"${self.profit[date_key]:.2f}",
            )
            self.hourly[spot] = False

    def calc_profit(self, seconds, price=2):
        return (seconds / 3600) * price
