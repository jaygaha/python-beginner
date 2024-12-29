# Countdown timer program

import time

# time.sleep(3)

# print("Time is up!")

my_time = int(input("Enter the time in seconds: "))

for i in range(my_time, 0):
    print(i)
    time.sleep(1)

print("Time is up!")

# Reverse

for i in range(my_time, 0, -1):
    secords = i % 60
    minutes = int(i / 60) % 60
    hours = int(i / 3600)
    print(f"{hours:02}:{minutes:02}:{secords:02}")
    time.sleep(1)

print("Time is up!")

