# Python system datetime module
import datetime

date = datetime.date(2025, 10, 31)
today = datetime.date.today()


print(date) # 2025-10-31
print(today) # 2025-01-01


time = datetime.time(23, 59, 59)
now = datetime.datetime.now()

nowFormatted = now.strftime("%H:%M:%S %d-%m-%Y")

print(time) # 23:59:59
print(now) # 2025-01-01 16:49:18.910042
print(nowFormatted) # 16:49:18 2025-01-01

target_datetime = datetime.datetime(2025, 10, 31, 23, 59, 59)
current_datetime = datetime.datetime.now()

if target_datetime < current_datetime:
    print("Target datetime has passed")
else:
    print("Target datetime has not passed")