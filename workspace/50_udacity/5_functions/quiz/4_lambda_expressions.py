# Lambda Expressions
# A lambda expression is an anonymous function

add_ten = lambda num: num + 10
add_ten_default = lambda num, defaddend=10: num + defaddend
add_ten_keyword = lambda num, defaddend=10: num + defaddend

print(add_ten(5))
print(add_ten_default(5))
print(add_ten_keyword(5))

##############################################################################
# Quiz: Lambda with Map
#
numbers = [
              [34, 63, 88, 71, 29],
              [90, 78, 51, 27, 45],
              [63, 37, 85, 46, 22],
              [51, 22, 34, 11, 18]
           ]

def mean(num_list):
    return sum(num_list) / len(num_list)

averages = list(map(mean, numbers))
print(averages)

# Converting to a lambda expression
averages = list(map(lambda num_list: sum(num_list) / len(num_list), numbers))
print(averages)

# Quiz: Lambda with Filter

cities = ["New York City", "Los Angeles", "Chicago", "Mountain View", "Denver", "Boston"]

def is_short(name):
    return len(name) < 10

short_cities = list(filter(is_short, cities))
print(short_cities)

# Converting to a lambda expression
short_cities = list(filter(lambda name: len(name) < 10, cities))
print(short_cities)
