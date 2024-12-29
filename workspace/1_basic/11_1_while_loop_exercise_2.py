# Python compund interest calculator

principal = 0
rate = 0
time = 0

while True:
    principal = float(input("Enter principal amount: "))
    if principal < 0:
        print("Principal amount must be greater than 0")
    else:
        break

while True:
    rate = float(input("Enter the interate rate: "))
    if rate < 0:
        print("Interest rate can't be less than 0")
    else:
        break

while True:
    time = int(input("Enter the time in year: "))
    if time < 0:
        print("Time can't be less than 0")
    else:
        break


total = principal * pow((1 + rate / 100),time)
print(f"Balance after {time} year/s : ${total:.2f}")