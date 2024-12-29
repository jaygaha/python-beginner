# 2d collection
# 2dlist = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

fruits =['apple', 'banana', 'cherry']
vegetables = ['carrot', 'potato', 'onion']
meats = ['fish', 'chicken', 'pork']

groceries = [fruits, vegetables, meats]

print(groceries)  # [['apple', 'banana', 'cherry'], ['carrot', 'potato', 'onion'], ['fish', 'chicken', 'pork']]

#indexing
print(groceries[0])  # ['apple', 'banana', 'cherry']
print(groceries[1][0])  # carrot

#iterating
for grocery in groceries:
    for food in grocery:
        print(food, end=",")
    print()