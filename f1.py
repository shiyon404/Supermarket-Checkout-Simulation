"""
 Part A of the Supermarket Checkout Lane Queue Simulation process
 involves generating lanes, adding customers to a lane,
 removing customers, opening/closing lanes, displaying lane status,
 and moving lanes.

 Created on Dec 26, 2023
 @author: Shiyon Suresh
"""

import time


# Class LaneResult print the output of Part A
class LaneResult:

    def __init__(self, __regular_checkout_data, __self_checkout_data):
        self.__regular_checkout_data = __regular_checkout_data
        self.__self_checkout_data = __self_checkout_data
        self.__starting_time = time.time()  # Initialing the starting time of this program
        self.__lane_saturated = False

    # get_slf_customer returns the total number of customers in self-checkout lane
    def get_slf_customer(self):
        no_customers_slf = len(self.__self_checkout_data)  # Total number of customers in self-checkout lane
        return no_customers_slf

    # get_reg_customer returns the total number of customers in regular-checkout lane
    def get_reg_customer(self):
        no_customers_reg = 0
        for new_data in self.__regular_checkout_data:
            if new_data != 'S1':
                # Adding number of customer of each lane to no_customers_reg
                no_customers_reg += len(self.__regular_checkout_data[new_data])
        return no_customers_reg

    # set_new_data sets new lane data to the initials
    def set_new_data(self, regular_checkout_data, self_checkout_data):
        self.__regular_checkout_data = regular_checkout_data
        self.__self_checkout_data = self_checkout_data

    # Printing the details of lanes
    def print_lane_management(self):
        current_time = time.time()  # Time when the function is called
        str_time = time.ctime(current_time)  # Time and date in full formate
        new_reg_customer_id = {"L1": [], "L2": [], "L3": [], "L4": [], "L5": []}  # New dict for adding new customers

        for data in self.__regular_checkout_data:
            # Adding 'C' to the customer's ID
            new_reg_customer_id[data] = ['C' + str(itemR) for itemR in self.__regular_checkout_data[data]]
            new_reg_customer_id[data] = ' '.join(new_reg_customer_id[data])

        # Adding 'C' to the customer's ID
        new_self_customer_id = ['C' + str(itemS) for itemS in self.__self_checkout_data]
        new_self_customer_id = ' '.join(new_self_customer_id)

        no_customers_slf = self.get_slf_customer()  # Total number of customers in self-checkout lane
        no_customers_reg = self.get_reg_customer()  # Total number of customers in regular-checkout lane
        # Total number of customers in self-checkout and regular-checkout lane
        no_customers = no_customers_slf + no_customers_reg
        self.__starting_time = time.time()

        # Prints out the lane data along with timestamp
        print(f"Total number of customers waiting to check out at: {str_time} is: {no_customers}")
        print(
            f"L1(Reg) -> {new_reg_customer_id['L1'] if len(self.__regular_checkout_data['L1']) != 0 else '**opened**'}"
            f"\nL2(Reg) -> {new_reg_customer_id['L2'] if len(self.__regular_checkout_data['L2']) != 0 else '**closed**'}"
            f"\nL3(Reg) -> {new_reg_customer_id['L3'] if len(self.__regular_checkout_data['L3']) != 0 else '**closed**'}"
            f"\nL4(Reg) -> {new_reg_customer_id['L4'] if len(self.__regular_checkout_data['L4']) != 0 else '**closed**'}"
            f"\nL5(Reg) -> {new_reg_customer_id['L5'] if len(self.__regular_checkout_data['L5']) != 0 else '**closed**'}"
            f"\nL6(Slf) -> {new_self_customer_id if len(self.__self_checkout_data) != 0 else '**opened**'} \n\n")

        if no_customers >= 40:  # Checking if the total no of customers is greater than 40
            self.__lane_saturated = True  # Reporting lane saturation
            print('**** Lane Saturation REPORTED *****\n\n')
        else:
            self.__lane_saturated = False


# Class LaneManagement manages the lane and their customer's data
class LaneManagement(LaneResult):

    def __init__(self, __regular_checkout_data, __self_checkout_data):
        super().__init__(__regular_checkout_data, __self_checkout_data)
        self.__started = False
        self.__item_data = {}  # Customer's items data
        self.__queue_data = {}  # Lane data with customer ID
        self.__added_id = []  # Avoid duplication
        self.__self_checkout_data = []  # Dict L1:no of customer
        self.__regular_checkout_data = {"L1": [], "L2": [], "L3": [], "L4": [], "L5": []}  # Dict L1:no of customer
        self.__lane_status = {"L1": True, "L2": False, "L3": False, "L4": False, "L5": False, "S1": True}  # Lane status
        # Dict of lane with customer id for removing queue system
        self.__remove_customer_data = {"L1": '', "L2": '', "L3": '', "L4": '', "L5": '', "S1": ''}
        self.__regular_checkout_time = {}  # Data of each customer's time to checkout at regular-checkout lane
        self.__self_checkout_time = {}  # Data of each customer's time to checkout at self-checkout lane

    # lane_startup prints out data when the system is starting up
    def lane_startup(self):
        current_time = time.time()
        str_time = time.ctime(current_time)

        print('#### Manager has Successfully Logged In #####')

        for times in range(6):
            remaining_sec = 6 - times
            time.sleep(1)
            print(f"SUPERMARKET NETWORK BOOTING IN {remaining_sec} SECONDS")

        time.sleep(1)
        print("SUPERMARKET NETWORK STARTED!")
        time.sleep(1)

        print(f"\nTotal number of customers waiting to check out at: {str_time} is: 0")
        print(
            f"L1(Reg) -> **opened**"
            f"\nL2(Reg) -> **closed**"
            f"\nL3(Reg) -> **closed**"
            f"\nL4(Reg) -> **closed**"
            f"\nL5(Reg) -> **closed**"
            f"\nL6(Slf) -> **opened**")

    # close_lane closes the lane if its empty
    def close_lane(self):
        for closing in self.__regular_checkout_data:
            # Check if the lane is empty and not L1(Because L1 and Slf 1 always will be open)
            if len(self.__regular_checkout_data[closing]) == 0 and closing != 'L1':
                self.__lane_status[closing] = False

    # move_lane moves customer from longest lane to shortest lane
    def move_lane(self):

        s_r_checkout = self.__regular_checkout_data  # Regular-checkout lane data
        s_r_checkout['S1'] = self.__self_checkout_data  # Self-checkout lane data
        # Sorting the data in terms of shortest lane
        asc_lane = dict(sorted(s_r_checkout.items(), key=lambda item: len(item[1])))
        # Sorting the data in terms of longest lane
        desc_lane = dict(sorted(s_r_checkout.items(), key=lambda item: len(item[1]), reverse=True))

        for shortest_lane in asc_lane:
            shortest_list = asc_lane[shortest_lane]  # Shortest lane data

            # Checking if the selected lane is open and not empty
            if self.__lane_status[shortest_lane] and len(shortest_list) > 0:
                longest_lane = list(desc_lane.keys())[0]  # The longest lane
                longest_list = list(desc_lane.values())[0]  # Customers in the longest lane
                #  Checking that the no of customers in the longest is less than no of customers in the shortest lane
                #  Also check if selected lane is full
                #  And avoid selecting S1(self-checkout) lane as shortest lane
                if (len(shortest_list) < len(longest_list)) and (shortest_lane != 'S1' and len(shortest_list) < 5):
                    cst_id = longest_list[-1]  # The last customer of the longest lane

                    if longest_lane == 'S1':
                        adding_dict = self.__regular_checkout_data
                        for addition_dict in adding_dict:
                            if shortest_lane == addition_dict:
                                adding_dict[shortest_lane].append(cst_id)  # Adding customer data to new lane
                                self.__self_checkout_data.remove(cst_id)  # Removing customer data from old lane
                                break

                    if longest_lane != 'S1':
                        removable_dict = self.__regular_checkout_data
                        adding_dict = self.__regular_checkout_data
                        for lane_name in removable_dict:
                            if longest_lane == lane_name and cst_id in removable_dict[longest_lane]:
                                for addition_dict in adding_dict:
                                    if shortest_lane in addition_dict:
                                        adding_dict[shortest_lane].append(cst_id)  # Adding customer data to new lane
                                        adding_dict[longest_lane].remove(cst_id)  # Removing customer data from old lane
                                        break

    # remove_customer removes customer from the lane after the checkout time
    def remove_customer(self):
        temp_lane = self.__regular_checkout_data  # Regular-checkout lane data
        for removable in temp_lane:
            selected_lane_data = self.__remove_customer_data[removable]
            lane_data = self.__regular_checkout_data[removable]  # Lane name
            if len(lane_data) > 0 and selected_lane_data == '':  # Checking if lane is empty or not
                first_customer_reg = lane_data[0]  # First customer of the lane
                # Calculates the time to checkout with selected lane
                time_for_checkout = 6 * self.__item_data[first_customer_reg]
                # Creating data of the customer to checkout
                self.__remove_customer_data[removable] = {'id': first_customer_reg, 'start_time': time.time(),
                                                          'exit_time': time_for_checkout}
            if len(lane_data) > 0 and selected_lane_data != '':  # Checking if lane is empty or not
                if (time.time() - selected_lane_data['start_time'] > selected_lane_data['exit_time']) and \
                        selected_lane_data['id'] in lane_data:  # Checking the time to remove the customer
                    # Removing customer data from lane data
                    self.__regular_checkout_data[removable].remove(selected_lane_data['id'])
                    self.__remove_customer_data[removable] = ''

        # Working with self-checkout lane data
        # Checking if lane is empty or not
        if len(self.__self_checkout_data) > 0 and self.__remove_customer_data['S1'] == '':
            first_customer_self = self.__self_checkout_data[0]  # First customer of the lane
            time_for_checkout = 4 * self.__item_data[
                first_customer_self]  # Calculates the time to checkout with selected lane
            # Creating data of the customer to checkout
            self.__remove_customer_data['S1'] = {'id': first_customer_self, 'start_time': time.time(), 'exit_time': time_for_checkout}

        # Checking the time to remove the customer
        if len(self.__self_checkout_data) > 0 and self.__remove_customer_data['S1'] != '':
            if (time.time() - float(self.__remove_customer_data['S1']['start_time']) > float(
                    self.__remove_customer_data['S1'][
                        'exit_time'])) and self.__remove_customer_data['S1']['id'] in self.__self_checkout_data:
                self.__self_checkout_data.remove(
                    self.__remove_customer_data['S1']['id'])  # Removing customer data from lane data
                self.__remove_customer_data['S1'] = ''

    # add_customer adds the customer to the customer data
    def add_customer(self, customer_data):
        self.__item_data.update(customer_data)  # Adding new item data to the self.__item_data
        self.__queue_data.update(customer_data)  # Adding new customer queue data to the self.__queue_data

    # enter_lane insert the customer into the lane
    def enter_lane(self, current_customer_id, lane_id):
        if lane_id == 'self':
            self.__self_checkout_data.append(current_customer_id)  # Adding customer to self-checkout lane
        else:
            self.__regular_checkout_data[lane_id].append(
                current_customer_id)  # Adding customer to regular-checkout lane
        super().set_new_data(self.__regular_checkout_data, self.__self_checkout_data)  # Setting new customer data

    # open_lane set the lane status as open
    def open_lane(self, lane_id):
        self.__lane_status[lane_id] = True

    # lane_queue process the customer in basics of their basket and lane situations
    def lane_queue(self, item_data):
        new_item_data = item_data  # Data of items in their basket
        for queueing in new_item_data:
            if new_item_data[queueing] < 10 and len(
                    self.__self_checkout_data) < 15:  # Checking item less than 10 & self-checkout customer less than 15
                self.enter_lane(queueing, 'self')  # Pushing the customer to self-checkout lane
            else:
                # Processing with regular-checkout lane
                for new_queue in self.__regular_checkout_data:
                    # When customer is less than 5 and status is open
                    if (len(self.__regular_checkout_data[new_queue]) < 5) and self.__lane_status[new_queue]:
                        self.enter_lane(queueing, new_queue)  # Adding customer to the selected lane
                        break

                    elif not self.__lane_status[new_queue]:  # Check if its closed
                        self.open_lane(new_queue)  # Open the new lane
                        # Sort the dict and allow the customer to join the shortest regular-checkout lane
                        self.__regular_checkout_data = {key: value for key, value in
                                                        sorted(self.__regular_checkout_data.items(),
                                                               key=lambda item: item[
                                                                   1])}
                        self.enter_lane(queueing, new_queue)  # Adding customer to the selected lane
                        break
