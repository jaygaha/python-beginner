# default argument = A default value for parameter
# default is used when that argument is omitted
# make your function more flexible, reduces number of arguments
# 1. positional, 2. default, 3. keyword, 4. arbitrary

import time

# default

def net_price (list_price, discount = 0, tax =0.05):
    return list_price * (1-discount) * (1 + tax)

# print(net_price(499, 0, 0.05)) # 523.95
# print(net_price(499, 0.1)) # 471.55500000000006
print(net_price(499, 0.1, 0)) # 449.1



def count(end, start = 0):
    for x in range(start, end+1):
        print(x)
        time.sleep(1)
    print("DONE")

# count(10)
count(30, 16)