# Concession stand program: a dictionary that stores the prices of different items in a concession stand.

# dictionary {key: value}

menu = {"popcorn": 5.99,"soda": 3.49,"hotdog": 7.49,"candy": 4.99,"chips": 2.99}

cart = []
total = 0

print("Welcome to the concession stand!")
for key, value in menu.items():
    print(f"{key:10}: ${value:.2f}")

print("-----------------------------")

while True:
    food = input("What would you like to order (q to quit)? ").lower()

    if (food == "q"):
        break
    elif menu.get(food) is not None:
        cart.append(food)
    else:
        print("Sorry, we don't have that item.")

print("----------Your Order--------------")
for food in cart:
    total += menu.get(food)
    print(food, end=" ")

print()
print(f"Total: ${total:.2f}")