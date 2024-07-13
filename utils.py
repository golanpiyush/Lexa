

import datetime
import os

def currentDay():
    # Get the current date
    today = datetime.datetime.now()
   
    # Get the day of the week as an integer (Monday is 0, Sunday is 6)
    day_index = today.weekday()
   
    # List of days of the week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
   
    # Return the day of the week as a string
    return days[day_index]

def ClearScreen():
    # Clear command-line screen based on OS
    if os.name == 'nt':   # for Windows
        _ = os.system('cls')
    elif os.name == 'posix':  # for Unix and Linux
        _ = os.system('clear')
    else:
        print("Unsupported OS. Cannot clear the screen.")
