# day.py

import datetime

def get_current_day():
    # Get the current date
    today = datetime.datetime.now()
   
    # Get the day of the week as an integer (Monday is 0, Sunday is 6)
    day_index = today.weekday()
   
    # List of days of the week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
   
    # Return the day of the week as a string
    return days[day_index]