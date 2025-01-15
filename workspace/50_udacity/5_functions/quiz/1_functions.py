# Functions
# Defining Functions
# headers: type, name, args, return
#
# print vs return
#
# this prints something, but does not return anything
def show_plus_ten(num):
    print(num + 10)

# this returns something
def add_ten(num):
    return(num + 10)

print('Calling show_plus_ten...')
return_value_1 = show_plus_ten(5)
print('Done calling')
print('This function returned: {}'.format(return_value_1))

print('\nCalling add_ten...')
return_value_2 = add_ten(5)
print('Done calling')
print('This function returned: {}'.format(return_value_2))


# default arguments
def add_ten_default(num, defaddend=10):
    return(num + defaddend)

print('Calling add_ten_default...')
return_value_3 = add_ten_default(5)
print('Done calling')
print('This function returned: {}'.format(return_value_3))


# keyword arguments

print('Calling add_ten_keyword...')
return_value_4 = add_ten_default(5, defaddend=5)
print('Done calling')
print('This function returned: {}'.format(return_value_4))


##############################################################################
# Quiz: Population Density Function
def population_density(population, area):
    return population / area

# test cases for your function
test1 = population_density(10, 1)
expected_result1 = 10
print("expected result: {}, actual result: {}".format(expected_result1, test1))

test2 = population_density(864816, 121.4)
expected_result2 = 7123.6902801
print("expected result: {}, actual result: {}".format(expected_result2, test2))

# Quiz: readable_timedelta
def readable_timedelta(days):
    # use integer division to get the number of weeks
    weeks = days // 7
    # use % to get the number of days that remain
    days = days % 7

    return '{} week(s) and {} day(s)'.format(weeks, days)

print(readable_timedelta(10)) # 1 week(s) and 3 day(s).
print(readable_timedelta(1)) # 0 week(s) and 1 day(s).
print(readable_timedelta(6)) # 0 week(s) and 6 day(s).
print(readable_timedelta(7)) # 1 week(s) and 0 day(s).
print(readable_timedelta(9)) # 1 week(s) and 2 day(s).
print(readable_timedelta(579)) # 82 week(s) and 5 day(s).
print(readable_timedelta(9311)) # 1330 week(s) and 1 day(s).
