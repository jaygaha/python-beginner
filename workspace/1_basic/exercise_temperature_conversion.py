# Temperatue Conversion

unit = input("Enter the unit of temperature (C)elsius or (F)ahrenheit: ")
temp = float(input("Enter the temperature: "))

if unit == "C":
    unit = round((9 * temp) / 5 + 32, 1)
    print(f"Temperature is {unit} F")
elif unit == "F":
    unit = round((temp - 32) * 5 / 9, 1)
    print(f"Temperature is {unit} C")
else:
    print(f"Invalid unit {unit} of measurement")