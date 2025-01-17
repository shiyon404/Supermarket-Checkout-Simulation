
# Supermarket Checkout Simulation

A Python-based supermarket checkout queue simulation system that manages customer flow, checkout lanes, and processing times.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Components](#components)
- [Authors](#authors)
- [License](#license)

## Overview
This simulation manages supermarket checkout processes with both self-service and cashier-operated lanes. It handles:
- Customer generation with random basket sizes
- Lane allocation and management
- Checkout time calculations
- Lottery ticket system for large purchases

## Features
- 🛍️ Dynamic customer generation
- 🏪 Multiple checkout lane types
- ⏱️ Real-time processing simulation
- 🎫 Lottery system for purchases ≥ 10 items
- 📊 Live queue monitoring
- 🔄 Automatic lane balancing

## Requirements
- Python 3.8+
- tkinter (for GUI)
- time module
- random module

## Installation
```sh
# Clone the repository
git clone https://github.com/shiyon404/Supermarket-Checkout-Simulation.git

# Navigate to project directory
cd Supermarket-Checkout-Simulation

# Run the simulation
python main.py
```

## Usage
1. Launch the application using main.py

2. Use the control panel buttons:
   - Start Simulation
   - Display F1/F2
   - Stop Simulation
   - Exit

## Components

### Lane Management (f1.py)
- Handles checkout lanes
- Processes customer flow
- Manages lane opening/closing
```python
# Example usage
lane_manager = LaneManagement({}, {})
lane_manager.lane_startup()
```

### Customer Generation (f2.py)
- Creates random customers
- Assigns basket sizes (1-30 items)
- Calculates checkout times
```python
# Example usage
customer = CustomerLayout({}, {})
customer.generate_customer()
```

### Main Simulation (main.py)
- Controls simulation flow
- Provides GUI interface
- Manages timing and events

## Authors
- Shiyon Suresh - Lane Management System
- Abhishek Soni - Customer Generation System

## License
This project is licensed under the MIT License
