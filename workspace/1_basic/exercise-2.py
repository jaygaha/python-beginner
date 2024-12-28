# Exercie 2 Shopping cart app

item = input("Enter the item you want to buy?: ")
price = float(input("Enter the price of the item: "))
quantity = int(input("Enter the quantity of the item: "))
total = price * quantity

print(f"You are buying {quantity} {item} at ${price} each. Total is ${total}")
#print(f"Total price for {quantity} {item} is ${total}")
