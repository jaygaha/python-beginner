# While Loops: Iterating over a Sequence

card_deck = [4, 11, 8, 5, 13, 2, 8, 10]
hand = []

## adds the last element of the card_deck list to the hand list
## until the values in hand add up to 17 or more
while sum(hand)  < 17:
    hand.append(card_deck.pop())

print(hand)

# number to find the factorial of
number = 6

# start with our product equal to one
product = 1

# track the current number being multiplied
current = 1

# write your while loop here
while current <= number:
    # multiply the product so far by the current number
    product *= current

    # increment current with each iteration until it reaches number
    current += 1

# print the factorial of number
print(product)

# use a for loop to find the factorial!
number = 6

# start with our product equal to one
product = 1

## calculate factorial of number with a for loop
for num in range(2, number + 1):
    product *= num
# for current in range(1, number + 1):
#     product *= current

# print the factorial of number
print(product)

print()

# Count By

start_num = 1 #provide some start number
end_num = 20 #provide some end number that you stop when you hit
count_by = 2 #provide some number to count by

# write a while loop that uses break_num as the ongoing number to
#   check against end_num
break_num = start_num

while break_num <= end_num:
    print(break_num)
    break_num += count_by

print(break_num)

# Count By Check

start_num = 45 #provide some start number
end_num = 44 #provide some end number that you stop when you hit
count_by = 3 #provide some number to count by

# write a condition to check that end_num is larger than start_num before looping
# write a while loop that uses break_num as the ongoing number to
#   check against end_num
break_num = start_num
result = ""

if start_num > end_num:
    result = "Oops! Looks like your start value is greater than the end value. Please try again."
else:
    # while break_num <= end_num:
    #     break_num += count_by
    break_num = start_num
    while break_num < end_num:
        break_num += count_by

    result = break_num

print(result)

print()
# Quiz: Nearest Square: finds the largest square number less than an integerlimit and stores it in a variable nearest_square
limit = 40
nearest_square = 0
n = 1  # Start with the smallest integer

# while True:
#     square = n * n  # Calculate the square of n
#     if square < limit:
#         nearest_square = square  # Update nearest_square if the square is less than limit
#         n += 1  # Increment n to check the next integer
#     else:
#         break  # Exit the loop if the square is not less than limit

# while n * n < limit:
#     nearest_square = n * n  # Update nearest_square with the current square
#     n += 1  # Increment n to check the next integer

while (n+1)**2 < limit:
    n += 1
nearest_square = n**2


print(nearest_square)  # Output: 36

# for vs while
#   for loops are ideal when the number of iterations is known in advance,
#   while loops are ideal when the number of iterations is unknown. when iterations need to continue untill a certain condition is met
#
# For: when you have an iterable collection (list, string, set, tuple, dictionary, range)
# While: while count <= 10, while user_input != 'quit'


# Question
# Which loop will be used for the folloing list
# Condition: Your code should add up the odd numbers in the list, but only up to the first 5 odd numbers together. If there are more than 5 odd numbers,
# you should stop at the fifth. If there are fewer than 5 odd numbers, add all of the odd numbers.
num_list = [422, 136, 524, 85, 96, 719, 85, 92, 10, 17, 312, 542, 87, 23, 86, 191, 116, 35, 173, 45, 149, 59, 84, 69, 113, 166]

# Answer
# While loop should be used
count_odd = 0
list_sum = 0
i = 0
len_num_list = len(num_list)

while (count_odd < 5) and (i < len_num_list):
    if num_list[i] % 2 != 0:
        list_sum += num_list[i]
        count_odd += 1
    i += 1

print ("The numbers of odd numbers added are: {}".format(count_odd))
print ("The sum of the odd numbers added is: {}".format(list_sum))

# Answer
# for loop
# for num in num_list:
#     print(num)

# # while loop
# count_odd = 0
# list_sum = 0
# i = 0
# len_num_list = len(num_list)

# while (count_odd < 5) and (i < len_num_list):
#     if num_list[i] % 2 != 0:
#         list_sum += num_list[i]
#         count_odd += 1
#     i += 1

# print ("The numbers of odd numbers added are: {}".format(count_odd))
# print ("The sum of the odd numbers added is: {}".format(list_sum))