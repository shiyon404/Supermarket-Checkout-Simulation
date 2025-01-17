"""
 Part C of the Supermarket Checkout Lane Queue Simulation
 is a combination of Part A and Part B. It consists of a simulation
 that runs the entire program for a certain amount of time and stops itself.

 Created on Jan 18, 2024
 @authors: Shiyon Suresh & Abhishek Soni
"""

import time
import tkinter as tk
import threading

from tkinter import messagebox  # Using the messagebox from tkinter
from f1 import LaneManagement  # Using class LaneManagement from f1
from f2 import CustomerLayout  # Using class CustomerLayout from f2


# Class Logbook create a frame with four button to control the simulation
class Logbook:

    def __init__(self, main):
        self.main = main
        self.main.title("Supermarket Lane System")
        self.f1 = LaneManagement({}, {})  # First initiation for class LaneManagement
        self.f2 = CustomerLayout({}, {})  # First initiation for class CustomerLayout

        self.simulation_started = False  # To check if the simulation is running
        self.lane_data = False  # To check if lane data is displaying
        self.customer_data = False  # To check if customer data is displaying

        # Create menu frame
        self.menu_frame = tk.Frame(self.main, width=150, bg="lightgray")
        self.menu_frame.pack(side="left", fill="y")

        # Populate menu frame with buttons
        button_width = 50
        button_height = 2

        self.button1 = tk.Button(self.menu_frame, text="Start Simulation", command=self.start_simulation, width=button_width, height=button_height)
        self.button2 = tk.Button(self.menu_frame, text="Display F1/F2", command=self.f1_f2, width=button_width, height=button_height)
        self.button3 = tk.Button(self.menu_frame, text="Stop Simulation", command=self.stop_simulation, width=button_width, height=button_height)
        self.exit_button = tk.Button(self.menu_frame, text="Exit", command=self.exit_program, width=button_width, height=button_height)

        # Making the buttons fill to the window
        self.button1.pack(pady=5, fill="both", expand=True)
        self.button2.pack(pady=5, fill="both", expand=True)
        self.button3.pack(pady=5, fill="both", expand=True)
        self.exit_button.pack(pady=5, fill="both", expand=True)

    # start_simulation starts the simulation
    def start_simulation(self):
        if not self.simulation_started:  # Check if simulation is started or not
            threading.Thread(target=self.generate_f3).start()
            self.simulation_started = True  # Setting the status of simulation
            messagebox.showinfo("Supermarket", "Starting simulation")
        elif self.simulation_started:
            messagebox.showinfo("Supermarket", "Simulation is already running")

    # f1_f2 displays the lane data and customer data from part F1 and F2
    def f1_f2(self):
        if not self.simulation_started:  # Check if simulation is running or not
            messagebox.showinfo("Supermarket", "Simulation is not running")
        elif self.simulation_started:
            if not self.lane_data:  # Checking if Customer data is displaying
                self.lane_data = True
                self.customer_data = False
                self.f2.enable_print_basket(False)  # Pushing the status to stop printing customer data
                messagebox.showinfo("Supermarket", "Lane data(F1) will start displaying within 10 seconds")
            elif self.lane_data:  # Checking if lane data is displaying
                self.customer_data = True
                self.lane_data = False
                self.f2.enable_print_basket(True)  # Pushing the status to start printing customer data
                messagebox.showinfo("Supermarket", "Customer data(F2) will start displaying within 30 seconds")

    # stop_simulation stops the simulation
    def stop_simulation(self):
        if self.simulation_started:  # Check if simulation is running or not
            self.simulation_started = False  # Set status to stop
            messagebox.showinfo("Supermarket", "Stopping the simulation")
        else:
            messagebox.showinfo("Supermarket", "Simulation is not running")

    # exit_program used to exit the program window and stops the simulation
    def exit_program(self):
        self.simulation_started = False  # Set status to stop
        self.main.destroy()  # Close the window

    # generate_f3 simulates the whole program
    def generate_f3(self):
        starting_time = time.time()  # Starting time of the program
        last_time_customer_generated = starting_time
        last_time_lane_data_generated = starting_time
        last_time_move_lane = starting_time
        cfg_customer_generation_timer = 30  # Interval to generate random number of customers
        cfg_lane_data_timer = 10  # Interval to print the lane data
        cfg_move_lane_data_timer = 30  # Interval to check moving of lane
        self.f1.lane_startup()
        time.sleep(3)
        self.f2.generate_customer()
        while self.simulation_started:  # The loop run till the simulation timer
            current_time = time.time()

            # Calculates the last time for each function
            elapsed_time_customer_generation = current_time - last_time_customer_generated
            elapsed_time_lane_data_generation = current_time - last_time_lane_data_generated
            elapsed_time_move_lane = current_time - last_time_move_lane

            if elapsed_time_lane_data_generation >= cfg_lane_data_timer:  # Checking time to print lane data
                if self.lane_data:  # Checking if displaying lane data is running (GUI)
                    self.f2.print_lane_management()
                self.f2.remove_customer()
                last_time_lane_data_generated = current_time  # reset the start time

            # Checking time to generate new customers
            elif elapsed_time_customer_generation >= cfg_customer_generation_timer:
                self.f2.generate_customer()
                if self.lane_data:  # Checking if displaying lane data is running (GUI)
                    self.f2.print_lane_management()
                last_time_customer_generated = current_time  # reset the start time

            if elapsed_time_move_lane >= cfg_move_lane_data_timer:  # Checking time for move lane
                self.f2.move_lane()
                last_time_move_lane = current_time

            time.sleep(1)  # Time sleep to cooldown the whole program for CPU

        print('##### END OF SIMULATION #####')


if __name__ == "__main__":
    window = tk.Tk()
    app = Logbook(window)
    window.mainloop()
