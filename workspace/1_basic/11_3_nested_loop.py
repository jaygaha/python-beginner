# nested loop: A loop inside another loop is called a nested loop.
# outer loop: The outer loop is responsible for iterating over the rows.
#   inner loop: The inner loop is responsible for iterating over the columns.

for i in range(3):
    for j in range(1, 10):
        print(j, end="")
    print() # print new line