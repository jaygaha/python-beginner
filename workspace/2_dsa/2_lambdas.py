# Lambdas: functions without a name/anonymous functions

# normal function
def add(a, b):
    return a + b

print(add(1, 2)) # 3

# lambda function

# add2 = lambda a, b: a + b

# print(add2(1, 2)) # 3
print((lambda a, b: a + b)(1, 2)) # 3

#Example
# higher order functions: functions that take other functions as arguments or return functions as results
def my_map(my_func, my_list):
    result = []
    for item in my_list:
        new_item = my_func(item)
        result.append(new_item)
    return result

nums = [1, 2, 3, 4, 5]

cuded = my_map(lambda x: x**3, nums)

print(cuded) # [1, 8, 27, 64, 125]