import tkinter as tk

# Constants for the MRAD adjustments
# Non-linear MRAD adjustments based on distance (both vertical and horizontal)
mrad_adjustments = {
    100: {'vertical': 0.0, 'horizontal': 0.2},
    150: {'vertical': 0.2, 'horizontal': 0.4},
    200: {'vertical': 0.5, 'horizontal': 0.5},
    250: {'vertical': 0.9, 'horizontal': 0.6},
    300: {'vertical': 1.4, 'horizontal': 0.8},
    350: {'vertical': 1.9, 'horizontal': 0.9},
    400: {'vertical': 2.4, 'horizontal': 1.1},
    450: {'vertical': 3.0, 'horizontal': 1.3},
    500: {'vertical': 3.7, 'horizontal': 1.4},
    550: {'vertical': 4.4, 'horizontal': 1.6},
    600: {'vertical': 5.2, 'horizontal': 1.8},
    650: {'vertical': 6.0, 'horizontal': 1.9},
    700: {'vertical': 6.9, 'horizontal': 2.1},
    750: {'vertical': 7.9, 'horizontal': 2.3},
    800: {'vertical': 9.9, 'horizontal': 2.5},
    850: {'vertical': 10.1, 'horizontal': 2.7},
    900: {'vertical': 11.3, 'horizontal': 3.0},
    950: {'vertical': 12.6, 'horizontal': 3.2},
    1000: {'vertical': 14.0, 'horizontal': 3.4},
}

# Constants for the MRAD adjustments per 10 meters
vertical_adjustments_per_10_meters = 0.0  # Default for when distance is not in the table

# Constants for the horizontal MRAD adjustments per 10 meters
horizontal_adjustments_per_10_meters = 0.0  # Default for when distance is not in the table

# Wind MRAD adjustment factor
wind_mrad_factor = 0.25

# Wind CW (Crosswind) adjustments based on angle
wind_cw_adjustments = {
    0: 0.0,
    20: 0.5,
    45: 0.8,
    90: 1.0
}

# Function to calculate MRAD adjustments (both vertical and horizontal)
def calculate_mrad_adjustments(distance_meters, closest_ranges, closest_mrad_values):
    # Find the two closest ranges above and below the target's range
    closest_range_below = max(r for r in closest_ranges if r <= distance_meters)
    closest_range_above = min(r for r in closest_ranges if r >= distance_meters)

    # Find the corresponding MRAD values for these ranges
    mrad_below = closest_mrad_values[closest_range_below]
    mrad_above = closest_mrad_values[closest_range_above]

    # Calculate the MRAD adjustments for the target distance
    vertical_adjustment = mrad_below['vertical'] + (distance_meters - closest_range_below) * (
        mrad_above['vertical'] - mrad_below['vertical']) / (closest_range_above - closest_range_below)

    horizontal_adjustment = mrad_below['horizontal'] + (distance_meters - closest_range_below) * (
        mrad_above['horizontal'] - mrad_below['horizontal']) / (closest_range_above - closest_range_below)

    # Round the adjustments to one decimal place
    vertical_adjustment = round(vertical_adjustment, 1)
    horizontal_adjustment = round(horizontal_adjustment / 4, 1)  # Divide by 4 for horizontal adjustment

    return vertical_adjustment, horizontal_adjustment

# Function to calculate side-to-side adjustment for wind
def calculate_wind_adjustment(ws, cw_angle, horizontal_adjustment_per_10_meters):
    # Calculate the horizontal adjustment due to wind
    wind_adjustment = (horizontal_adjustment_per_10_meters / 10) * ws * wind_cw_adjustments[cw_angle]

    # Round the adjustment to one decimal place
    wind_adjustment = round(wind_adjustment, 1)

    return wind_adjustment

# Function to calculate adjustments and update the result labels
def calculate_adjustments():
    try:
        # Get user inputs from the entry widgets
        target_distance = float(entry_distance.get())
        wind_speed = float(entry_wind_speed.get())
        cw_angle = int(entry_cw_angle.get())

        # Calculate vertical and horizontal adjustments
        vertical_adjustment, horizontal_adjustment = calculate_mrad_adjustments(target_distance, list(mrad_adjustments.keys()), mrad_adjustments)

        # Calculate wind adjustment
        wind_adjustment = calculate_wind_adjustment(wind_speed, cw_angle, horizontal_adjustments_per_10_meters)

        # Update the result labels
        result_vertical.config(text=f"Vertical Adjustment: {vertical_adjustment} MRADs")
        result_horizontal.config(text=f"Horizontal Adjustment: {horizontal_adjustment} MRADs")
        result_wind.config(text=f"Horizontal Adjustment (Wind): {wind_adjustment} MRADs")

    except ValueError:
        result_vertical.config(text="Please enter valid numeric values.")
        result_horizontal.config(text="")
        result_wind.config(text="")

# Create the main window
window = tk.Tk()
window.title("Bullet Drop Calculator for L129A1/146gr-0.308-7.62mm")

# Create and configure labels, entry widgets, and buttons
label_distance = tk.Label(window, text="Target Distance (meters):")
entry_distance = tk.Entry(window)
label_wind_speed = tk.Label(window, text="Wind Speed (m/s):")
entry_wind_speed = tk.Entry(window)
label_cw_angle = tk.Label(window, text="Crosswind Angle (0, 20, 45, 90 degrees):")
entry_cw_angle = tk.Entry(window)
calculate_button = tk.Button(window, text="Calculate", command=calculate_adjustments)

result_vertical = tk.Label(window, text="")
result_horizontal = tk.Label(window, text="")
result_wind = tk.Label(window, text="")

# Place widgets on the grid
label_distance.grid(row=0, column=0)
entry_distance.grid(row=0, column=1)
label_wind_speed.grid(row=1, column=0)
entry_wind_speed.grid(row=1, column=1)
label_cw_angle.grid(row=2, column=0)
entry_cw_angle.grid(row=2, column=1)
calculate_button.grid(row=3, column=0, columnspan=2)
result_vertical.grid(row=4, column=0, columnspan=2)
result_horizontal.grid(row=5, column=0, columnspan=2)


# Start the GUI main loop
window.mainloop()

# Made by MikeDaGamer
