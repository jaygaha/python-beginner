# format specifiers = {:flags} format a value based on what flags are passed

# .(number)f = round to that many decimal places (fixed-point)
# :(number) = allocate that many spaces for the value
# :03 = alloate and zero pad that many spaces for the value
# :< = left align
# :> = right align
# :^ = center align
# :+ = use a plus sign to indicate if the number is positive
# :- = use a minus sign to indicate if the number is negative
# := =  place sign to leftmost position
# :_ = use an underscore as a thousand separator
# :, = use a comma as a thousand separator
# :b = binary
#  : = insert a spacebefore positive numbers

price1 = 3.14159
price2 = -987.654
price3 = 12.34

print(f"Price 1: ${price1:.2f}")
print(f"Price 2: ${price2:.2f}")
print(f"Price 3: ${price3:.2f}")

print(f"Price 1: ${price1:010}")
print(f"Price 2: ${price2:010}")
print(f"Price 3: ${price3:010}")

print(f"Price 1: ${price1:+}")
print(f"Price 2: ${price2:+}")
print(f"Price 3: ${price3:+}")