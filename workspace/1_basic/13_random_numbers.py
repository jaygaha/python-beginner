# random number

import random

# dice
number = random.randint(1, 6)

print(number)

low = 1
high = 100

number = random.randint(low, high)

print(number)

# random float
rand_num_float = random.random()

print(rand_num_float)

# choices
options = ("Rock", "Paper", "Scissors")

option = random.choice(options)

print(option)

# shuffle

cards = ["2","3","4","5","6","7","8","9","10","J","Q","K", "A"]

random.shuffle(cards)

print(cards)

