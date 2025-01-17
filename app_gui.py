import tkinter as tk
from tkinter import messagebox
import time

import data


class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Lot System")
        self.hourly_spots = 15
        self.monthly_spots = 5

        # Create parking lot instances
        self.parking = data.ParkingSpace()

        # Create the UI elements
        self.create_ui()

        # To track the selected button
        self.selected_button = None
        self.selected_spot = None

    def create_ui(self):
        # Frame for hourly parking spots
        self.hourly_frame = tk.Frame(self.root)
        self.hourly_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(self.hourly_frame, text="Hourly Parking", font=("Arial", 12)).grid(
            row=0, column=0, columnspan=5
        )
        self.hourly_buttons = []
        for i in range(self.hourly_spots):
            button = tk.Button(
                self.hourly_frame,
                text="Empty",
                bg="green",
                width=10,
                height=3,
                command=lambda i=i: self.select_spot(i, "hourly")
            )
            button.grid(row=(i // 5) + 1, column=i % 5, padx=5, pady=5)
            self.hourly_buttons.append(button)

        # Frame for monthly parking spots
        self.monthly_frame = tk.Frame(self.root)
        self.monthly_frame.grid(row=1, column=0, padx=10, pady=10)

        tk.Label(self.monthly_frame, text="Monthly Parking", font=("Arial", 12)).grid(
            row=0, column=0, columnspan=5
        )
        self.monthly_buttons = []
        for i in range(self.monthly_spots):
            button = tk.Button(
                self.monthly_frame,
                text="Empty",
                bg="blue",
                width=10,
                height=3,
                command=lambda i=i: self.select_spot(i, "subscription"),
            )
            button.grid(row=(i // 5) + 1, column=i % 5, padx=5, pady=5)
            self.monthly_buttons.append(button)

        # Entry form for license plate and driver name
        self.form_frame = tk.Frame(self.root)
        self.form_frame.grid(row=2, column=0, padx=10, pady=10)

        tk.Label(self.form_frame, text="License Plate:").grid(row=0, column=0)
        self.license1_entry = tk.Entry(self.form_frame)
        self.license1_entry.grid(row=0, column=1)

        # Rent Spot Form
        self.rent_form_frame = tk.Frame(self.root)
        # Adjust column to be next to the form
        self.rent_form_frame.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.rent_form_frame, text="License Plate:").grid(
            row=0, column=0)
        self.license2_entry = tk.Entry(self.rent_form_frame)
        self.license2_entry.grid(row=0, column=1)

        tk.Label(self.rent_form_frame, text="Driver Name:").grid(
            row=1, column=0)
        self.driver_name_entry = tk.Entry(self.rent_form_frame)
        self.driver_name_entry.grid(row=1, column=1)

        tk.Label(self.rent_form_frame, text="Spot:").grid(row=2, column=0)
        self.spot_entry = tk.Entry(self.rent_form_frame)
        self.spot_entry.grid(row=2, column=1)

        tk.Label(self.rent_form_frame, text="Duration (months):").grid(
            row=3, column=0)
        self.duration_entry = tk.Entry(self.rent_form_frame)
        self.duration_entry.grid(row=3, column=1)

        self.rent_button = tk.Button(
            self.rent_form_frame, text="Rent Spot", command=self.rent_spot
        )
        self.rent_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Radio buttons for selecting parking rate
        self.rate_var = tk.StringVar(value="hourly")

        self.park_button = tk.Button(
            self.form_frame, text="Park Car", command=self.park_car
        )
        self.park_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.remove_button = tk.Button(
            self.form_frame, text="Remove Car", command=self.remove_car
        )
        self.remove_button.grid(row=4, column=0, columnspan=2)

    def select_spot(self, spot_index, spot_type):
        if self.selected_button:
            self.selected_button.config(highlightthickness=0)

        if spot_type == "hourly":
            self.selected_button = self.hourly_buttons[spot_index]
        elif spot_type == "monthly":
            self.selected_button = self.monthly_buttons[spot_index]

        self.selected_button.config(
            highlightbackground="black", highlightthickness=3)
        self.selected_spot = (spot_type, spot_index)

    def park_car(self):
        license_plate = self.license1_entry.get()

        if not license_plate:
            messagebox.showerror(
                "Error", "Please provide license plate."
            )
            return

        self.parking.park(license_plate)

        self.update_monthly_parking_ui()
        self.update_hourly_parking_ui()

        # Reset the selected button's appearance
        if self.selected_button:
            self.selected_button.config(highlightthickness=0)
        self.selected_spot = None
        self.selected_button = None

        # Clear the input fields
        self.license1_entry.delete(0, tk.END)

    def remove_car(self):
        if self.selected_spot is None:
            messagebox.showerror("Error", "Please select a parking spot.")
            return

        (spot_type, spot_index) = self.selected_spot
        self.parking.remove_car(spot_index, spot_type)

        self.update_monthly_parking_ui()
        self.update_hourly_parking_ui()

        # Reset the selected button's appearance
        if self.selected_button:
            self.selected_button.config(highlightthickness=0)
        self.selected_spot = None
        self.selected_button = None

    def rent_spot(self):
        license = self.license2_entry.get()
        driver_name = self.driver_name_entry.get()
        spot = int(self.spot_entry.get())
        duration = int(self.duration_entry.get())

        # if not license or not driver_name or not spot or not duration:
        #     messagebox.showerror("Error", "Please fill out all fields.")
        #     return

        # Assuming the parking class has a rent method
        vec = data.Vehicle(license, spot, driver_name,
                           True,  time.time(), duration)
        
        if self.parking.rent_spot(vec):
            messagebox.showinfo("Success", "Spot rented successfully!")
        else:
            messagebox.showerror(
                "Error", "Failed to rent the spot. Please try again.")
            
        self.update_hourly_parking_ui()
        self.update_monthly_parking_ui()

        # Clear the rent form
        self.license2_entry.delete(0, tk.END)
        self.driver_name_entry.delete(0, tk.END)
        self.spot_entry.delete(0, tk.END)
        self.spot_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def update_hourly_parking_ui(self):
        for index, spot in enumerate(self.parking.hourly):
            button = self.hourly_buttons[index]
            if isinstance(spot, data.Vehicle):
                button.config(bg="red", text=spot.license)
            else:
                button.config(bg="green", text="Empty")

    def update_monthly_parking_ui(self):
        for index, spot in enumerate(self.parking.subscription):
            button = self.monthly_buttons[index]
            if isinstance(spot["vehicle"], data.Vehicle):
                button.config(bg="grey", text=spot["vehicle"].license)
            else:
                button.config(bg="blue", text="Empty")

    def update_profit(self):
        self.profit_label.config(
            text=f"Profit: ${(self.parking_monthly.profit +
                              self.parking_hourly.profit):.3f}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()
