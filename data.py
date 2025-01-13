import time 
import logging

log_file="parking_log.csv"

class ParkingInfo:
    def __init__(self, car_license, driver_name):
        self.car_license = car_license
        self.driver_name = driver_name
        self.start_time = None

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
                



if __name__ == "__main__":

    car1 = ParkingInfo(car_license="ABC123", driver_name="Alice")
    car2 = ParkingInfo(car_license="XYZ789", driver_name="Bob")
    car3 = ParkingInfo(car_license="LMN456", driver_name="Charlie")
    car4 = ParkingInfo(car_license="KKP000", driver_name="Charlie")

    parking_lot = ParkingSpace(total_spots=10)

    # Test parking cars
    print("\nTesting parking cars:")
    parking_lot.park_car(car1)  # Should park car1 at spot 0
    parking_lot.park_car(car2)  # Should park car2 at spot 1
    parking_lot.park_car(car3)  # Should park car3 at spot 2
    print(parking_lot)

    time.sleep(5)
    parking_lot.remove_car(car2)
    print(parking_lot)

    parking_lot.park_car(car4)
    print(parking_lot)

    parking_lot.park_car(ParkingInfo(car_license="ZZZ000", driver_name="David"))
    print(parking_lot)

    print(f"PROFIT: {parking_lot.profit}")