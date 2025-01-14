import time 
import logging

log_file="parking_log.csv"

class ParkingInfo:
    def __init__(self, car_license, driver_name, is_sub):
        self.car_license = car_license
        self.driver_name = driver_name
        self.start_time = None
        self.is_sub = is_sub

    def __eq__(self, other):
        if isinstance(other, ParkingInfo):
            return self.car_license == other.car_license
        return False

    def __repr__(self):
        return f"ParkingInfo(car_license='{self.car_license}')"


class ParkingSpace:
    def __init__(self, total_spots):
        # Initialize a parking space with all spots empty
        self.spots = [False] * total_spots  # False means empty
        self.profit = 0

    def park_car(self, ParkingInfo_obj):
        # Park a car in the first available spot
        for index, spot in enumerate(self.spots):
            if not spot:  # Check if the spot is available (empty)
                self.spots[index] = ParkingInfo_obj
                ParkingInfo_obj.start_time  = time.time()
                logging._log_entry(log_file, 
                                   "INBOUND",
                                   ParkingInfo_obj.car_license,
                                   ParkingInfo_obj.driver_name,
                                   index,
                                   time.strftime("%Y-%m-%d %H:%M:%S"),
                                   "")
                return  # Stop once the car is parked
        print("No available spots.")

    def park_car_sub(self, ParkingInfo_obj):
        try:
            index = self.spots.index(ParkingInfo_obj)
            # Deregister after monthly subscribtion ends.
            if (time.time() - ParkingInfo_obj.start_time) > 2592000: # 60*60*24*30 seconds in a month
                self.spots[index] = False
                return self.park_car_sub(ParkingInfo_obj)

            logging._log_entry(log_file, 
                                   "INBOUND SUBSCRIBER",
                                   ParkingInfo_obj.car_license,
                                   ParkingInfo_obj.driver_name,
                                   index,
                                   time.strftime("%Y-%m-%d %H:%M:%S"),
                                   "")
        except:
            self.park_car(ParkingInfo_obj)
            self.profit += 50

    def remove_car(self, ParkingInfo_obj):
        # Find the spot index where the car with the given id is located
        try:
            index = self.spots.index(ParkingInfo_obj)
            self.spots[index] = False  # Mark the spot as empty
            profit = self.calc_profit(ParkingInfo_obj.start_time, time.time())
            self.profit += profit
            logging._log_entry(log_file, 
                               "OUTBOUND",
                               ParkingInfo_obj.car_license,
                               ParkingInfo_obj.driver_name,
                               index,
                               "",
                               time.strftime("%Y-%m-%d %H:%M:%S"),
                               profit)       
        except :
            print(f"Car with license {ParkingInfo_obj} not found.")

    def calc_profit(self, start_sec, stop_sec, price=2):
        diff = stop_sec - start_sec
        return (diff/3600) * price

    def __repr__(self):
        # Return a string representation of the parking space status
        return (f"ParkingSpace({', '.join(repr(item) for item in self.spots)}), "
                "\n"
                f"Available spots: {self.spots.count(False)}")

class CarRegistry:
    cars = {}

    @staticmethod
    def get_or_create(car_license, driver_name, is_sub):
        if car_license not in CarRegistry.cars:
            CarRegistry.cars[car_license] = ParkingInfo(
                car_license, driver_name, is_sub
            )
        return CarRegistry.cars[car_license]


if __name__ == "__main__":
    # Use CarRegistry to create or retrieve cars
    car1 = CarRegistry.get_or_create("ABC123", "Alice", False)
    car2 = CarRegistry.get_or_create("XYZ789", "Bob", False)
    car3 = CarRegistry.get_or_create("LMN456", "Charlie", False)
    car4 = CarRegistry.get_or_create("KKP000", "Charlie", False)
    car5 = CarRegistry.get_or_create("ZZZ000", "David", True)
    car6 = CarRegistry.get_or_create("AAA333", "Alex", True)
    car7 = CarRegistry.get_or_create("AAA333", "Alex", True)  # Same license as car6

    # Create parking spaces
    parking_hourly = ParkingSpace(total_spots=10)
    parking_monthly = ParkingSpace(total_spots=5)

    # Test parking cars
    print("\nTesting parking cars:")
    parking_hourly.park_car(car1)  # Should park car1 at spot 0
    parking_hourly.park_car(car2)  # Should park car2 at spot 1
    parking_hourly.park_car(car3)  # Should park car3 at spot 2
    print(parking_hourly)

    time.sleep(3)
    parking_hourly.remove_car(car2)  # Remove car2
    print(parking_hourly)

    parking_hourly.park_car(car4)  # Park car4
    print(parking_hourly)

    # Test parking subscribers
    parking_monthly.park_car_sub(car5)  # Park subscriber car5
    print(parking_monthly)
    parking_monthly.park_car_sub(car6)  # Park subscriber car6
    parking_monthly.park_car_sub(car6)  # Should not add a new spot
    parking_monthly.park_car_sub(car6)  # Should not add a new spot
    print(parking_monthly)

    time.sleep(5)  # Simulate passage of time
    parking_monthly.park_car_sub(car7)  # Same car as car6
    print(parking_monthly)

    # Calculate and display total profit
    print(f"PROFIT: {parking_hourly.profit + parking_monthly.profit}")
