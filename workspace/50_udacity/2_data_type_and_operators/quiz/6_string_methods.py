# String methods: same as functions, but they are called on a string, not on a variable with dot notation
name = "ram bahadur"
age = 20
email = "ram@gmail.com"

print("{} is {} years old and has email {}".format(name.capitalize(), age, email))

# split: splits a string into a list of strings
new_string = "ram bahadur is 20 years old, and has email ram@gmail.com"
print(new_string.split()) # ['ram', 'bahadur', 'is', '20', 'years', 'old,', 'and', 'has', 'email', 'ram@gmail.com']

# maxsplit: splits a string into a list of strings, but only splits at the first maxsplit number of splits
print(new_string.split(maxsplit=1)) # ['ram', 'bahadur is 20 years old, and has email ram@gmail.com']

# dot notation: accesses a string attribute
print(new_string.split(",")) # ['ram bahadur is 20 years old', ' and has email ram@gmail.com']

# None: returns None if the string is empty
print(new_string.split(",", maxsplit=1)) # ['ram bahadur is 20 years old', ' and has email ram@gmail.com']

verse = "If you can keep your head when all about you\n  Are losing theirs and blaming it on you,\nIf you can trust yourself when all men doubt you,\n  But make allowance for their doubting too;\nIf you can wait and not be tired by waiting,\n  Or being lied about, don’t deal in lies,\nOr being hated, don’t give way to hating,\n  And yet don’t look too good, nor talk too wise:"
print(verse)

# Use the appropriate functions and methods to answer the questions above
# Bonus: practice using .format() to output your answers in descriptive messages!
#
# What is the length of the string variable verse?
print(len(verse)) # 362

split_verse = verse.split()
print(split_verse)
# ['If', 'you', 'can', 'keep', 'your', 'head', 'when', 'all', 'about', 'you', 'Are', 'losing', 'theirs', 'and', 'blaming', 'it', 'on', 'you,',
# 'If', 'you', 'can', 'trust', 'yourself', 'when', 'all', 'men', 'doubt', 'you,', 'But', 'make', 'allowance', 'for', 'their', 'doubting', 'too;',
#  'If', 'you', 'can', 'wait', 'and', 'not', 'be', 'tired', 'by', 'waiting,', 'Or', 'being', 'lied', 'about,', 'don’t', 'deal', 'in', 'lies,', 'Or',
#  'being', 'hated,', 'don’t', 'give', 'way', 'to', 'hating,', 'And', 'yet', 'don’t', 'look', 'too', 'good,', 'nor', 'talk', 'too', 'wise:']

# What is the index of the first occurrence of the word 'and' in verse?
# Hint: use the .index() method
print(verse.index("and")) # 65
print(verse.find("and")) # 65

# What is the index of the last occurrence of the word 'you' in verse?
# Hint: use the .rindex() method
print(verse.rindex("you")) # 186
print(verse.rfind("you")) # 186

# What is the count of occurrences of the word 'you' in the verse
# Hint: use the .count() method
print(verse.count("you")) # 8

print()

# VERSION 2: use the appropriate functions and methods to answer the questions above
print(verse, "\n")

message = "Verse has a length of {} characters.\nThe first occurence of the \
word 'and' occurs at the {}th index.\nThe last occurence of the word 'you' \
occurs at the {}th index.\nThe word 'you' occurs {} times in the verse."

length = len(verse)

first_idx = verse.find('and')
last_idx = verse.rfind('you')
count = verse.count('you')

print(message.format(length, first_idx, last_idx, count))
