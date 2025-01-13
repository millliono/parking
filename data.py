class ParkingInfo:
    def __init__(self, car_license, driver_name, start_time, stop_time):
        self.car_license = car_license
        self.driver_name = driver_name
        self.start_time = start_time
        self.stop_time = stop_time

    # Define the __eq__ method to compare two ParkingInfo objects
    def __eq__(self, other):
        if isinstance(other, ParkingInfo):
            return (self.car_license == other.car_license and
                    self.driver_name == other.driver_name and
                    self.start_time == other.start_time and
                    self.stop_time == other.stop_time)
        return False

    def __repr__(self):
        # return (f"ParkingInfo(car_license='{self.car_license}', driver_name='{self.driver_name}', "
        #         f"start_time={self.start_time}, stop_time={self.stop_time})")
        return f"ParkingInfo(car_license='{self.car_license}')"


class ParkingSpace:
    def __init__(self, total_spots):
        # Initialize a parking space with all spots empty
        self.spots = [False] * total_spots  # False means empty

    def park_car(self, ParkingInfo_obj):
        # Park a car in the first available spot
        for index, spot in enumerate(self.spots):
            if not spot:  # Check if the spot is available (empty)
                self.spots[index] = ParkingInfo_obj
                print(f"Car parked at spot {index}.")
                return  # Stop once the car is parked
        print("No available spots.")

    def remove_car(self, ParkingInfo_obj):
        # Find the spot index where the car with the given id is located
        try:
            index = self.spots.index(ParkingInfo_obj)
            self.spots[index] = False  # Mark the spot as empty
            print(f"Car with ID {ParkingInfo_obj} removed from spot {index}.")
        except :
            print(f"Car with ID {ParkingInfo_obj} not found.")

    def __repr__(self):
        # Return a string representation of the parking space status
        return (f"ParkingSpace({', '.join(repr(item) for item in self.spots)}), "
                "\n"
                f"Available spots: {self.spots.count(False)}")
                



if __name__ == "__main__":

    car1 = ParkingInfo(car_license="ABC123", driver_name="Alice", start_time="2025-01-01 08:00", stop_time="2025-01-01 10:00")
    car2 = ParkingInfo(car_license="XYZ789", driver_name="Bob", start_time="2025-01-01 09:00", stop_time="2025-01-01 11:00")
    car3 = ParkingInfo(car_license="LMN456", driver_name="Charlie", start_time="2025-01-01 10:00", stop_time="2025-01-01 12:00")
    car4 = ParkingInfo(car_license="KKP000", driver_name="Charlie", start_time="2025-01-01 10:00", stop_time="2025-01-01 12:00")

    parking_lot = ParkingSpace(total_spots=10)

    # Test parking cars
    print("\nTesting parking cars:")
    parking_lot.park_car(car1)  # Should park car1 at spot 0
    parking_lot.park_car(car2)  # Should park car2 at spot 1
    parking_lot.park_car(car3)  # Should park car3 at spot 2
    print(parking_lot)

    parking_lot.remove_car(car2)
    print(parking_lot)

    parking_lot.park_car(car4)
    print(parking_lot)

    parking_lot.park_car(ParkingInfo(car_license="ZZZ000", driver_name="David", start_time="2025-01-01 12:00", stop_time="2025-01-01 14:00"))
    # Should print "No available spots."



    # Test if we can compare two ParkingInfo objects
    print("\nTesting ParkingInfo comparison:")
    car4 = ParkingInfo(car_license="ABC123", driver_name="Alice", start_time="2025-01-01 08:00", stop_time="2025-01-01 10:00")
    car5 = ParkingInfo(car_license="XYZ789", driver_name="Bob", start_time="2025-01-01 09:00", stop_time="2025-01-01 11:00")

    print(f"car1 == car4: {car1 == car4}")  # Should print True
    print(f"car1 == car5: {car1 == car5}")  # Should print False
