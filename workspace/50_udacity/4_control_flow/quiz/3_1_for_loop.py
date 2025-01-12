# For Loops: Iterating over a Sequence
# 2 kinds of loops: for loops and while loops

# for loop

for i in range(10):
    print(i)
    print('I\'m in a loop')


sentence = ["the", "quick", "brown", "fox", "jumped", "over", "the", "lazy", "dog"]

# Write a for loop to print out each word in the sentence list, one word per line

for word in sentence:
    print(word)

# Write a for loop using range() to print out multiples of 5 up to 30 inclusive

for i in range(5, 31, 5):
    print(i)

print()

# Quiz: Create usernames
names = ["Joey Tribbiani", "Monica Geller", "Chandler Bing", "Phoebe Buffay"]
usernames = []

for name in names:
    username = name.lower().replace(" ", "_")
    usernames.append(username)

print(usernames)


names = ["Joey Tribbiani", "Monica Geller", "Chandler Bing", "Phoebe Buffay"]

for name in names:
    name = name.lower().replace(" ", "_") # it will not change the original list because it is a copy

print(names)

# Quiz: Modify Usernames with Range
names = ["Joey Tribbiani", "Monica Geller", "Chandler Bing", "Phoebe Buffay"]

for i in range(len(names)):
    names[i] = names[i].lower().replace(" ", "_")

print(names)

# Quiz: Tag Counter
tokens = ['<greeting>', 'Hello World!', '</greeting>']
count = 0

# write your for loop here
# hint if a string is an XML tag if it begins with a left angle bracket "<" and ends with a right angle bracket ">"
for token in tokens:
    if token.startswith("<") and token.endswith(">"):
        count += 1
# for token in tokens:
#     if token[0] == '<' and token[-1] == '>':
#         count += 1

print(count)

# Quiz: Create a HTML List
items = ['first string', 'second string']
html_str = "<ul>\n"  # "\ n" is the character that marks the end of the line, it does
                     # the characters that are after it in html_str are on the next line

# write your code here
for item in items:
    html_str += "<li>{}</li>\n".format(item)

html_str += "</ul>"

print(html_str)

print()

print(list(range(4)))
print(list(range(4,8)))
print(list(range(4,10,2)))
print(list(range(0,-5))) # empty list because the range is empty

colors = ['Red', 'Blue', 'Green', 'Purple']
lower_colors = []

for color in colors:
    #finish this part
    lower_colors.append(color.lower())

print(lower_colors)