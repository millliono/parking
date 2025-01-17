import time


class Vehicle:
    def __init__(self, license, spot=None, driver_name=None, is_sub=False, start=None, duration=None):
        self.license = license
        self.spot = spot
        self.driver_name = driver_name
        self.is_sub = is_sub
        self.start = start
        self.duration = duration

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
        self.subscription = [
            {"occupied": False, "vehicle": False} for _ in range(5)]

    def park(self, license):
        reg = self.find_registered(license)
        if reg:
            self.subscription[reg]["occupied"] = True
        else:
            # Park a car in the first available spot
            vec = Vehicle(license)
            for index, spot in enumerate(self.hourly):
                if not spot:  # Check if the spot is available (empty)
                    self.hourly[index] = vec
                    vec.spot = index
                    vec.start = time.time()
                    return  # Stop once the car is parked
            print("No available spots.")

    def find_registered(self, license):
        for index, item in enumerate(self.subscription):
            vehicle = item["vehicle"]
            if vehicle and vehicle.license == license:
                return index
        return False

    def rent_spot(self, vehicle):
        if vehicle.spot > 0 and self.subscription[vehicle.spot]["vehicle"] == False:
            self.subscription[vehicle.spot]["vehicle"] = vehicle
            return True
        return False

    def remove_car(self, spot, spot_type):
        if spot_type == "monthly":
            self.subscription[spot]["occupied"] = False
        elif spot_type == "hourly":
            self.hourly[spot] = False  # Mark the spot as empty

    def calc_profit(self, start_sec, stop_sec, price=2):
        diff = stop_sec - start_sec
        return (diff / 3600) * price

    def __repr__(self):
        # Return a string representation of the parking space status
        return (f"Hourly({', '.join(repr(item) for item in self.hourly)}), "
                "\n"
                f"Subscription({', '.join(repr(item) for item in self.subscription)})")


if __name__ == "__main__":
    parking_space = ParkingSpace()

    # Create some vehicles
    vehicle1 = Vehicle(license="ABC123", driver_name="Alice")
    vehicle2 = Vehicle(license="XYZ789", driver_name="Bob")
    vehicle3 = Vehicle(license="ZZY998", driver_name="Patty")
    sub_vehicle1 = Vehicle(license="SUB001", spot=0,
                           is_sub=True, driver_name="Charlie")
    sub_vehicle2 = Vehicle(license="SUB002", spot=2,
                           is_sub=True, driver_name="Noris")

    parking_space.park(vehicle1.license)
    parking_space.park(vehicle2.license)
    parking_space.park(vehicle3.license)

    parking_space.rent_spot(sub_vehicle1)
    parking_space.rent_spot(sub_vehicle2)

    print(parking_space)

    parking_space.remove_car(sub_vehicle1.spot, "subscription")

    print(parking_space)

    print("\nFinal parking space status:")
    print(parking_space)
