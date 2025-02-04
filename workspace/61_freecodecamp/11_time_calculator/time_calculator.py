# Build a Time Calculator Project
#
# Write a function named add_time that takes in two required parameters and one optional parameter:
#
#     a start time in the 12-hour clock format (ending in AM or PM)
#     a duration time that indicates the number of hours and minutes
#     (optional) a starting day of the week, case insensitive
#
# The function should add the duration time to the start time and return the result.
#
# If the result will be the next day, it should show (next day) after the time. If the result will be more than one day later, it should show (n days later) after the time, where "n" is the number of days later.
#
# If the function is given the optional starting day of the week parameter, then the output should display the day of the week of the result. The day of the week in the output should appear after the time and before the number of days later.
#
# Below are some examples of different cases the function should handle. Pay close attention to the spacing and punctuation of the results.
#
# add_time('3:00 PM', '3:10')
# Returns: 6:10 PM
#
# add_time('11:30 AM', '2:32', 'Monday')
# # Returns: 2:02 PM, Monday
#
# add_time('11:43 AM', '00:20')
# # Returns: 12:03 PM
#
# add_time('10:10 PM', '3:30')
# # Returns: 1:40 AM (next day)
#
# add_time('11:43 PM', '24:20', 'tueSday')
# # Returns: 12:03 AM, Thursday (2 days later)
#
# add_time('6:30 PM', '205:12')
# # Returns: 7:42 AM (9 days later)

def add_time(current_time, duration, day=None):

  # define helper variable
  days_note = ""
  days_name = ""
  week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
  changing_format = {"AM":"PM", "PM":"AM"}

  # get time detail (hour, minute, and format) for each time params
  current_time_hour = int(current_time.split(" ")[0].split(":")[0])
  current_time_format = current_time.split(" ")[1]
  duration_hour = int(duration.split(":")[0])
  next_time_minutes = int(current_time.split(" ")[0].split(":")[1]) + int(duration.split(":")[1])

  # check if minute more than 60 and convert to hour if minute > 60
  if next_time_minutes > 60:
    next_time_minutes -= 60
    duration_hour += 1

  # calcutate next time hour, format and total days
  count_hours = (current_time_hour + duration_hour) % 12
  count_days = (current_time_hour + duration_hour) // 24
  count_format = (current_time_hour + duration_hour) % 24

  days_later = (count_days + 1) if (current_time_hour + duration_hour) >= 12 and current_time_format == "PM" else count_days
  next_time_hours = count_hours if count_hours != 0 else 12
  next_time_format = changing_format[current_time_format] if count_format >= 12 else current_time_format

  # set hour to 0 if current time format == PM and current time hour + duration hour == 12
  next_time_hours = 0 if (current_time_hour + duration_hour) == 12 and current_time_format == "PM" else next_time_hours

  # set days later note
  if days_later > 0:
    days_note = " (next day)" if days_later == 1 else f" ({days_later} days later)"

  # get current day
  if day:
    current_day_index = week.index(day.capitalize())
    reset_week = week[current_day_index:] + week[:current_day_index]
    next_day_index = (days_later % 7) if days_later > len(reset_week) else days_later
    days_name = f", {reset_week[next_day_index]}"

  return f"{next_time_hours}:{str(next_time_minutes).zfill(2)} {next_time_format}{days_name}{days_note}"


if __name__ == '__main__':
    print(add_time('3:00 PM', '3:10'))
    print(add_time('11:30 AM', '2:32', 'Monday'))
    print(add_time('11:43 AM', '00:20'))
    print(add_time('10:10 PM', '3:30'))
    print(add_time('11:43 PM', '24:20', 'tueSday'))
    print(add_time('6:30 PM', '205:12'))
