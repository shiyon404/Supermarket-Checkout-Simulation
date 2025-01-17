"""
 Part B of the Supermarket Checkout Lane Queue Simulation
 generates random numbers of customers with random items
 in their baskets. The code calculates the time it takes
 for customers to check out and checks if they have won the lottery.
 Once this is done, the data is pushed to Part A of this project.

 Created on Dec 23, 2023
 @author: Abhishek Soni
"""

import random
from f1 import LaneManagement, LaneResult  # Using two classes from Part A that is f1.py


# Class CustomerDetail process the data of generate customer
class CustomerDetail:

    def __init__(self):
        self.no_of_items = 0  # Number of items in the customer's basket
        self.customer_id = 0  # Current customer ID
        self.__self_checkout_estimate_time = 0  # Time for self-checkout
        self.__cashier_checkout_estimate_time = 0  # Time for regular-checkout

        # print_basket is used to print the output of Part B

    def print_basket(self, no_of_items, customer_id):
        self.no_of_items = no_of_items  # Setting new customer's items
        self.customer_id = customer_id  # Setting new customer's ID
        lottery_choice = False
        lottery_output = 'Hard Luck, no lottery ticket this time!'

        self.__self_checkout_estimate_time = 4 * self.no_of_items  # Self-Service checkout time
        self.__cashier_checkout_estimate_time = 6 * self.no_of_items  # Cashier till checkout time

        if self.no_of_items >= 10:  # Checking if the no of item is greater than 10
            lottery_choice = random.choice([True, False])

        if lottery_choice:  # Checking if the player won the lottery
            lottery_output = 'You are lucky, Won a lottery ticket!'

        # Printing the out of Part B
        print(f"### Customer Details ###"
              f"\nC{self.customer_id} -> Number of Items in basket: {self.no_of_items}"
              f"\nLottery Result: {lottery_output}"
              f"\nTime to process basket at cashier till: {self.__cashier_checkout_estimate_time} seconds"
              f"\nTime to process basket at self-service till: {self.__self_checkout_estimate_time} seconds\n")


# Class CustomerLayout generate random customer and their number of items in their basket
class CustomerLayout(CustomerDetail, LaneManagement, LaneResult):

    def __init__(self, reg_data, self_id):
        self.__no_of_customers = 0
        self.__customer_id = 0  # Customer's ID
        self.__customer_data = {}  # Customer's data
        self.__self_checkout_estimate_time = {}
        self.__cashier_checkout_estimate_time = {}
        self.__no_of_total_customer = 0
        self.is_printing_basket = False  # State for printing customer data(GUI)
        LaneManagement.__init__(self, reg_data, self_id)  # Initiating Class LaneManagement
        CustomerDetail.__init__(self)  # Initiating Class LaneManagement

    # enable_print_basket set the status of displaying customer data(GUI)
    def enable_print_basket(self, state):
        self.is_printing_basket = state  # Set the status of display

    # generate_customer generate customer's data and pushes to Part A
    def generate_customer(self):
        total_customers_slf = super().get_slf_customer()  # Getting total number of customers in self-checkout lane
        total_customers_reg = super().get_reg_customer()  # Getting total number of customers in regular-checkout lane

        self.__no_of_total_customer = total_customers_slf + total_customers_reg  # Total number of customers in queue

        # Checking if the program is running for first time
        if self.__no_of_customers == 0:
            self.__no_of_customers = 10  # Initial customers of number 10
        else:
            self.__no_of_customers = random.randint(1, 10)  # No of random customer 1-10
        # Addition of new customer and current customers
        no_of_new_customer = self.__no_of_customers + self.__no_of_total_customer

        # Avoiding adding new customers if the lane will be full after that
        if no_of_new_customer <= 40:  # Checking if new random customer can join or not
            for a in range(self.__no_of_customers):
                random_items = random.randint(1, 30)  # No of Basket Item 1-30

                # Checking if the generated number of player with their basket can join self or regular lane
                if (random_items < 5 and total_customers_slf < 15) or total_customers_reg < 25:
                    # Adding customer ID to itself to create unique customer id to avoid duplication
                    self.__customer_id += 1
                    self.__customer_data[self.__customer_id] = random_items  # Setting new customer's data

                    if self.is_printing_basket:  # Checking if displaying customer data(GUI)
                        # Pushing data to Class CustomerDetail.print_basket()
                        super().print_basket(random_items, self.__customer_id)

                    # Pushing data to Class LaneManagement.add_customer()
                    super().add_customer({self.__customer_id: random_items})

                    # Pushing data to Class LaneManagement.lane_queue()
                    super().lane_queue({self.__customer_id: random_items})
