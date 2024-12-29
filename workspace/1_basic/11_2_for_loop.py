# for loop: for loop is used to iterate over a sequence (list, tuple, string) or other iterable objects.

# 1: range
for i in range(1, 11):
    print(i)

# reverse order
for  i in reversed(range(1, 11)):
    print(i)

print("HappY New Year")

# range(start, stop, step)

for i in range(1, 11, 2):
    print(i) # 1, 3, 5, 7, 9

for i in range(1,21)
    if i == 13:
        continue
    else:
        print(i)


# 2: string
credit_card = "1234-5678-9012-3456"

for i in credit_card:
    print(i) # 1, 2, 3, 4, -, 5, 6, 7, 8, -, 9, 0, 1, 2, -, 3, 4, 5, 6