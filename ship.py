import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ShipBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ship Ticket Booking System")
        self.root.geometry("500x550")
        self.root.configure(padx=20, pady=20)

        # Try to use a cleaner theme if available
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')

        # Configure styles
        style.configure("TLabel", font=("Arial", 10))
        style.configure("Header.TLabel", font=("Arial", 16, "bold"), foreground="#2c3e50")

        # ----- Header -----
        header = ttk.Label(root, text="🚢 Ocean Voyager Booking", style="Header.TLabel")
        header.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # ----- Input Fields -----
        self.ports = ["Miami, USA", "Nassau, Bahamas", "San Juan, PR",
                      "London, UK", "Barcelona, Spain", "Rome, Italy", "Athens, Greece"]

        # Passenger Name
        ttk.Label(root, text="Passenger Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(root, textvariable=self.name_var, width=30)
        self.name_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        # Source Port
        ttk.Label(root, text="Source Port:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.source_var = tk.StringVar()
        self.source_combo = ttk.Combobox(root, textvariable=self.source_var, values=self.ports, state="readonly", width=27)
        self.source_combo.grid(row=2, column=1, sticky=tk.W, pady=5)

        # Destination Port
        ttk.Label(root, text="Destination Port:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.dest_var = tk.StringVar()
        self.dest_combo = ttk.Combobox(root, textvariable=self.dest_var, values=self.ports, state="readonly", width=27)
        self.dest_combo.grid(row=3, column=1, sticky=tk.W, pady=5)

        # Travel Class
        ttk.Label(root, text="Travel Class:").grid(row=4, column=0, sticky=tk.NW, pady=5)
        self.travel_class_var = tk.StringVar(value="Economy")

        class_frame = ttk.Frame(root)
        class_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(class_frame, text="Economy (Base Price)", variable=self.travel_class_var, value="Economy").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(class_frame, text="Business (+ $200)", variable=self.travel_class_var, value="Business").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(class_frame, text="Luxury Suite (+ $500)", variable=self.travel_class_var, value="Luxury Suite").pack(anchor=tk.W, pady=2)

        # Number of Tickets
        ttk.Label(root, text="Number of Tickets:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.tickets_var = tk.IntVar(value=1)
        self.tickets_spin = ttk.Spinbox(root, from_=1, to=10, textvariable=self.tickets_var, width=5, state="readonly")
        self.tickets_spin.grid(row=5, column=1, sticky=tk.W, pady=5)

        # ----- Buttons -----
        button_frame = ttk.Frame(root)
        button_frame.grid(row=6, column=0, columnspan=2, pady=25)

        self.calc_btn = ttk.Button(button_frame, text="Calculate Fare", command=self.calculate_fare, width=15)
        self.calc_btn.grid(row=0, column=0, padx=10)

        self.book_btn = ttk.Button(button_frame, text="Book Ticket", command=self.book_ticket, state=tk.DISABLED, width=15)
        self.book_btn.grid(row=0, column=1, padx=10)

        # ----- Result Summary -----
        self.result_var = tk.StringVar()
        self.result_label = ttk.Label(root, textvariable=self.result_var, justify=tk.LEFT, foreground="#2980b9")
        self.result_label.grid(row=7, column=0, columnspan=2, pady=5, sticky=tk.W)

        self.total_fare = 0

    def calculate_fare(self):
        source = self.source_var.get()
        dest = self.dest_var.get()
        name = self.name_var.get().strip()

        if not name:
            messagebox.showwarning("Missing Information", "Please enter the passenger's name.")
            return

        if not source or not dest:
            messagebox.showwarning("Missing Information", "Please select both Source and Destination ports.")
            return

        if source == dest:
            messagebox.showwarning("Invalid Route", "Source and Destination ports cannot be the same.")
            return

        t_class = self.travel_class_var.get()
        num_tickets = self.tickets_var.get()

        # Base fare calculation logic
        base_route_price = 300  # Default base price

        # Adjust base route price based on inter-continental vs local (simplified logic)
        # using the string lengths as a fake distance metric for demonstration
        distance = abs(len(source) - len(dest)) + 1
        route_fare = base_route_price + (distance * 15)

        # Class upgrades
        class_addons = {
            "Economy": 0,
            "Business": 200,
            "Luxury Suite": 500
        }

        fare_per_ticket = route_fare + class_addons.get(t_class, 0)
        self.total_fare = fare_per_ticket * num_tickets

        summary = (
            f"--- Booking Summary ---\n\n"
            f"Passenger: {name}\n"
            f"Route: {source} ➔ {dest}\n"
            f"Class: {t_class}\n"
            f"Tickets: {num_tickets}\n"
            f"Fare per ticket: ${fare_per_ticket:,.2f}\n"
            f"Total Amount: ${self.total_fare:,.2f}"
        )
        self.result_var.set(summary)
        self.book_btn.config(state=tk.NORMAL)

    def book_ticket(self):
        name = self.name_var.get().strip()
        messagebox.showinfo(
            "Booking Confirmed",
            f"Ticket successfully booked for {name}!\n\n"
            f"Amount paid: ${self.total_fare:,.2f}\n"
            f"Have a great voyage! 🚢"
        )
        self.reset_form()

    def reset_form(self):
        self.name_var.set("")
        self.source_combo.set('')
        self.dest_combo.set('')
        self.travel_class_var.set("Economy")
        self.tickets_var.set(1)
        self.result_var.set("")
        # Disable book button until fare is calculated again
        self.book_btn.config(state=tk.DISABLED)
        self.total_fare = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = ShipBookingApp(root)
    # Center the window on screen
    root.eval('tk::PlaceWindow . center')
    root.mainloop()