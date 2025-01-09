# Lists: Methods
#
# 1. list.append(item)
# 2. list.extend(iterable)
# 3. list.insert(index, item)
# 4. list.pop(index)
# 5. list.remove(item)
# 6. list.reverse()
# 7. list.sort()
# 8. list.index(item)
# 9. list.count(item)
# 10. list.copy()
# 11. list.clear()
# 12. list.count(item)
# 13. list.max(item)
# 14. list.min(item)
# 15. list.sum(item)
# 16. list.sorted(item)

# What would the output of the following code be? (Treat the comma in the multiple choice answers as newlines.)
a = [1, 5, 8]
b = [2, 6, 9, 10]
c = [100, 200]

print(max([len(a), len(b), len(c)]))
print(min([len(a), len(b), len(c)]))


# What would the output of the following code be? (Treat the comma in the multiple choice answers as newlines.)

names = ["Carol", "Albert", "Ben", "Donna"]
print(" & ".join(sorted(names)))

# What would the output of the following code be? (Treat the commas in the multiple choice answers as newlines.)

names = ["Carol", "Albert", "Ben", "Donna"]
names.append("Eugenia")
print(sorted(names))

# Choose the correct syntax to slice each of the following elements from the list:
arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
print(arr[2:6])
print(arr[:3])
print(arr[4:])
