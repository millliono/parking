import tkinter as tk
from tkinter import messagebox
import data
from datetime import datetime


class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Lot System")
        self.hourly_spots = 15
        self.monthly_spots = 5

        self.parking = data.ParkingSpace()
        self.create_ui()

        self.selected_button = None
        self.selected_spot = None

    def create_ui(self):
        # Frame for hourly parking spots
        self.hourly_frame = tk.Frame(self.root)
        self.hourly_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        tk.Label(self.hourly_frame, text="Hourly Parking", font=("Arial", 12)).grid(
            row=0, column=0, columnspan=5
        )
        self.hourly_buttons = []
        for i in range(self.hourly_spots):
            button = tk.Button(
                self.hourly_frame,
                text="Empty",
                bg="green",
                width=8,  # Reduced width
                height=2,  # Reduced height
                command=lambda i=i: self.select_spot(i, "hourly"),
            )
            button.grid(
                row=(i // 5) + 1, column=i % 5, padx=2, pady=2
            )  # Reduced padding
            self.hourly_buttons.append(button)

        # Frame for monthly parking spots
        self.monthly_frame = tk.Frame(self.root)
        self.monthly_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        tk.Label(self.monthly_frame, text="Monthly Parking", font=("Arial", 12)).grid(
            row=0, column=0, columnspan=5
        )
        self.monthly_buttons = []
        self.monthly_legends = []
        for i in range(self.monthly_spots):
            button = tk.Button(
                self.monthly_frame,
                text="Empty",
                bg="blue",
                width=8,  # Reduced width
                height=2,  # Reduced height
                command=lambda i=i: self.select_spot(i, "subscription"),
            )
            button.grid(
                row=(i // 5) + 1, column=i % 5, padx=2, pady=2
            )  # Reduced padding
            self.monthly_buttons.append(button)

            legend = tk.Label(
                self.monthly_frame, text="", font=("Arial", 10)
            )  # Smaller font
            legend.grid(row=(i // 5) + 2, column=i % 5)
            self.monthly_legends.append(legend)

        # Create a frame for all forms
        self.forms_frame = tk.Frame(self.root)
        self.forms_frame.grid(row=2, column=0, columnspan=2, pady=5)

        # Park Car Form (Left side)
        self.park_form_frame = tk.Frame(self.forms_frame)
        self.park_form_frame.grid(row=0, column=0, padx=5)

        tk.Label(self.park_form_frame, text="License Plate:").grid(
            row=0, column=0, sticky="e"
        )
        self.license1_entry = tk.Entry(self.park_form_frame, width=15)
        self.license1_entry.grid(row=0, column=1)

        tk.Label(self.park_form_frame, text="Date (YYYY-MM-DD):").grid(
            row=1, column=0, sticky="e"
        )
        self.date1_entry = tk.Entry(self.park_form_frame, width=15)
        self.date1_entry.grid(row=1, column=1)

        tk.Label(self.park_form_frame, text="Time (HH:MM):").grid(
            row=2, column=0, sticky="e"
        )
        self.time1_entry = tk.Entry(self.park_form_frame, width=15)
        self.time1_entry.grid(row=2, column=1)

        self.park_button = tk.Button(
            self.park_form_frame, text="Park Car", command=self.park_car, width=12
        )
        self.park_button.grid(row=3, column=0, columnspan=2, pady=2)

        # Remove car Form (Middle)
        self.remove_form_frame = tk.Frame(self.forms_frame)
        self.remove_form_frame.grid(row=0, column=1, padx=5)

        tk.Label(self.remove_form_frame, text="Date (YYYY-MM-DD):").grid(
            row=1, column=0, sticky="e"
        )
        self.date2_entry = tk.Entry(self.remove_form_frame, width=15)
        self.date2_entry.grid(row=1, column=1)

        tk.Label(self.remove_form_frame, text="Time (HH:MM):").grid(
            row=2, column=0, sticky="e"
        )
        self.time2_entry = tk.Entry(self.remove_form_frame, width=15)
        self.time2_entry.grid(row=2, column=1)

        self.remove_button = tk.Button(
            self.remove_form_frame, text="Remove Car", command=self.remove_car, width=12
        )
        self.remove_button.grid(row=4, column=0, columnspan=2, pady=2)

        # Rent Spot Form (Right side)
        self.rent_form_frame = tk.Frame(self.forms_frame)
        self.rent_form_frame.grid(row=0, column=2, padx=5)

        tk.Label(self.rent_form_frame, text="License Plate:").grid(
            row=0, column=0, sticky="e"
        )
        self.license3_entry = tk.Entry(self.rent_form_frame, width=15)
        self.license3_entry.grid(row=0, column=1)

        tk.Label(self.rent_form_frame, text="Driver Name:").grid(
            row=1, column=0, sticky="e"
        )
        self.driver_name_entry = tk.Entry(self.rent_form_frame, width=15)
        self.driver_name_entry.grid(row=1, column=1)

        tk.Label(self.rent_form_frame, text="Spot:").grid(row=2, column=0, sticky="e")
        self.spot_entry = tk.Entry(self.rent_form_frame, width=15)
        self.spot_entry.grid(row=2, column=1)

        tk.Label(self.rent_form_frame, text="Start Date (YYYY-MM-DD):").grid(
            row=3, column=0, sticky="e"
        )
        self.date3_entry = tk.Entry(self.rent_form_frame, width=15)
        self.date3_entry.grid(row=3, column=1)

        tk.Label(self.rent_form_frame, text="Duration (months):").grid(
            row=4, column=0, sticky="e"
        )
        self.duration_entry = tk.Entry(self.rent_form_frame, width=15)
        self.duration_entry.grid(row=4, column=1)

        self.rent_button = tk.Button(
            self.rent_form_frame, text="Rent Spot", command=self.rent_spot
        )
        self.rent_button.grid(row=5, column=0, columnspan=2, pady=5)

        self.profit_frame = tk.Frame(self.root)
        self.profit_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.profit_text = tk.Text(self.profit_frame, height=5, width=40)
        self.profit_text.pack(side=tk.LEFT)

        scrollbar = tk.Scrollbar(self.profit_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.profit_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.profit_text.yview)

    def update_profit(self):
        self.profit_text.delete(1.0, tk.END)

        total_profit = sum(self.parking.profit.values())
        self.profit_text.insert(tk.END, f"Total Profit: ${total_profit:.2f}\n\n")

        self.profit_text.insert(tk.END, "Daily Breakdown:\n")
        for date, amount in sorted(self.parking.profit.items()):
            self.profit_text.insert(tk.END, f"{date}: ${amount:.2f}\n")

    def select_spot(self, spot_index, spot_type):
        if self.selected_button:
            self.selected_button.config(highlightthickness=0)

        if spot_type == "hourly" and spot_index < len(self.hourly_buttons):
            self.selected_button = self.hourly_buttons[spot_index]
        elif spot_type == "subscription" and spot_index < len(self.monthly_buttons):
            self.selected_button = self.monthly_buttons[spot_index]
        else:
            messagebox.showerror("Error", "Invalid spot selected.")
            self.selected_button = None
            self.selected_spot = None
            return

        # Highlight the selected button
        self.selected_button.config(highlightbackground="black", highlightthickness=3)
        self.selected_spot = (spot_type, spot_index)

    def park_car(self):
        license_plate = self.license1_entry.get()
        date_str = self.date1_entry.get()
        time_str = self.time1_entry.get()

        if not license_plate:
            messagebox.showerror("Error", "Please fill the license plate!")
            return

        if date_str and time_str:
            datetime_str = f"{date_str} {time_str}"
            dt_object = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        else:
            dt_object = datetime.now()

        self.parking.park(license_plate, dt_object)

        self.update_monthly_parking_ui()
        self.update_hourly_parking_ui()

        # Reset the selected button's appearance
        if self.selected_button:
            self.selected_button.config(highlightthickness=0)
        self.selected_spot = None
        self.selected_button = None

        # Clear the input fields
        self.license1_entry.delete(0, tk.END)
        self.date1_entry.delete(0, tk.END)
        self.time1_entry.delete(0, tk.END)

    def remove_car(self):
        date_str = self.date2_entry.get()
        time_str = self.time2_entry.get()

        if self.selected_spot is None:
            messagebox.showerror("Error", "Please select a parking spot.")
            return

        if date_str and time_str:
            datetime_str = f"{date_str} {time_str}"
            dt_object = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        else:
            dt_object = datetime.now()

        (spot_type, spot_index) = self.selected_spot
        self.parking.remove_car(spot_index, spot_type, dt_object)

        self.update_monthly_parking_ui()
        self.update_hourly_parking_ui()
        self.update_profit()

        # Reset the selected button's appearance
        if self.selected_button:
            self.selected_button.config(highlightthickness=0)
        self.selected_spot = None
        self.selected_button = None

        self.date2_entry.delete(0, tk.END)
        self.time2_entry.delete(0, tk.END)

    def rent_spot(self):
        license = self.license3_entry.get()
        driver_name = self.driver_name_entry.get()
        spot = self.spot_entry.get()
        date_str = self.date3_entry.get()
        duration = self.duration_entry.get()

        if not license or not driver_name or not spot or not date_str or not duration:
            messagebox.showerror("Error", "Please fill the form.")
            return

        vec = data.Vehicle(
            license,
            int(spot),
            driver_name,
            True,
            datetime.strptime(date_str, "%Y-%m-%d"),
        )

        if self.parking.rent_spot(vec, int(duration)):
            messagebox.showinfo("Success", "Spot rented successfully!")
            self.update_hourly_parking_ui()
            self.update_monthly_parking_ui()
            self.update_profit()  # Update profit display
        else:
            messagebox.showerror("Error", "Failed to rent the spot. Please try again.")

        # Clear the rent form
        self.license3_entry.delete(0, tk.END)
        self.driver_name_entry.delete(0, tk.END)
        self.spot_entry.delete(0, tk.END)
        self.date3_entry.delete(0, tk.END)
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
            legend = self.monthly_legends[index]
            if isinstance(spot["vehicle"], data.Vehicle):
                if spot["occupied"]:
                    button.config(bg="grey", text=spot["vehicle"].license)
                else:
                    button.config(bg="blue", text="Empty")
                legend.config(text=spot["vehicle"].license)  
            else:
                button.config(bg="blue", text="Empty")
                legend.config(text="") 



if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()
