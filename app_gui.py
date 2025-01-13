import tkinter as tk
from tkinter import messagebox

import data

class ParkingApp:
    def __init__(self, root, total_spots=10):
        self.root = root
        self.root.title("Parking Lot System")
        self.total_spots = total_spots
        
        # Create the parking lot
        self.parking_lot = data.ParkingSpace(total_spots)
        
        # Create the UI elements
        self.create_ui()

        # To track the selected button
        self.selected_button = None
        
    def create_ui(self):
        # Frame for parking spots
        self.parking_frame = tk.Frame(self.root)
        self.parking_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Create a grid of parking spots (buttons)
        self.buttons = []
        for i in range(self.total_spots):
            button = tk.Button(self.parking_frame, text="Empty", bg="green", width=10, height=3,
                               command=lambda i=i: self.select_spot(i))
            button.grid(row=i//5, column=i%5, padx=5, pady=5)
            self.buttons.append(button)
        
        # Entry form for license plate and driver name
        self.form_frame = tk.Frame(self.root)
        self.form_frame.grid(row=1, column=0, padx=10, pady=10)
        
        tk.Label(self.form_frame, text="License Plate:").grid(row=0, column=0)
        self.license_entry = tk.Entry(self.form_frame)
        self.license_entry.grid(row=0, column=1)

        tk.Label(self.form_frame, text="Driver Name:").grid(row=1, column=0)
        self.driver_entry = tk.Entry(self.form_frame)
        self.driver_entry.grid(row=1, column=1)

        self.park_button = tk.Button(self.form_frame, text="Park Car", command=self.park_car)
        self.park_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.remove_button = tk.Button(self.form_frame, text="Remove Car", command=self.remove_car)
        self.remove_button.grid(row=3, column=0, columnspan=2)

        # Profit label
        self.profit_label = tk.Label(self.root, text=f"Profit: ${self.parking_lot.profit:.2f}")
        self.profit_label.grid(row=2, column=0, padx=10, pady=10)
        
    def select_spot(self, spot_index):
        """ Select a parking spot when clicking on it """
        if self.selected_button:
            # Reset the previous selected button's appearance
            self.selected_button.config(highlightthickness=0)
        
        # Select the new button and add a black border
        self.selected_button = self.buttons[spot_index]
        self.selected_button.config(highlightbackground="black", highlightthickness=3)
        self.selected_spot = spot_index

    def park_car(self):
        license_plate = self.license_entry.get()
        driver_name = self.driver_entry.get()

        if not license_plate or not driver_name:
            messagebox.showerror("Error", "Please provide both license plate and driver name.")
            return
        
        # Create ParkingInfo object
        car_info = data.ParkingInfo(license_plate, driver_name)
        
        self.parking_lot.park_car(car_info)
        
        # Update UI to show parked car
        self.update_parking_lot_ui()

        # Reset the selected button's appearance
        if self.selected_button:
            self.selected_button.config(highlightthickness=0)

        # Clear the selected spot
        self.selected_spot = None
        self.selected_button = None
        
        # Clear the input fields
        self.license_entry.delete(0, tk.END)
        self.driver_entry.delete(0, tk.END)

    def remove_car(self):
        if self.selected_spot is None:
            messagebox.showerror("Error", "Please select a parking spot.")
            return
        
        car_info = self.parking_lot.spots[self.selected_spot]

        # Remove the car from the parking lot
        self.parking_lot.remove_car(car_info)
        
        # Update UI to reflect the car removal
        self.update_parking_lot_ui()

        # Reset the selected button's appearance
        if self.selected_button:
            self.selected_button.config(highlightthickness=0)

        # Clear the selected spot
        self.selected_spot = None
        self.selected_button = None

        # Clear the input fields
        self.license_entry.delete(0, tk.END)
        self.driver_entry.delete(0, tk.END)

    def update_parking_lot_ui(self):
        """ Update the UI to reflect the parking lot status """
        for index, spot in enumerate(self.parking_lot.spots):
            button = self.buttons[index]
            if isinstance(spot, data.ParkingInfo):
                button.config(bg="red", text=spot.car_license)
            else:
                button.config(bg="green", text="Empty")
        
        # Update profit label
        self.profit_label.config(text=f"Profit: ${self.parking_lot.profit:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()

