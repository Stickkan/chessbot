from functions import *

try:
    # Take user input as a string
    user_input = input("Enter the depth level (1-6): ")

    # Convert the string to an integer
    depth_level = int(user_input)

    # Check if the entered value is within the allowed range
    if 1 <= depth_level <= 6:
        print("Invalid input. Please enter an integer between 1 and 6.")

except ValueError:
    print("Invalid input. Please enter a valid integer for the depth level.")


main_one_agent(b, depth_level, False)