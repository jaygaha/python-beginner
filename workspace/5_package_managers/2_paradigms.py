# Python programming paradigms
# Python supports four main programming paradigms: imperative, functional, procedural, and object-oriented.

# 1. Imperative programming
# Imperative programming is a programming paradigm that uses statements that change a program's state.

characters = ['P', 'y', 't', 'h', 'o', 'n']
result = ''
print(result) # _blank_

result = result + characters[0]
print(result) # P

result = result + characters[1]
print(result) # Py

result = result + characters[2]
print(result) # Pyt

result = result + characters[3]
print(result) # Pyth

result = result + characters[4]
print(result) # Pytho

result = result + characters[5]
print(result) # Python

# in above example, we are changing the state of the program by adding characters to the result variable.

# Shorter version is done using for loop (also imperative programming)
response = ''
for character in characters:
    response += character
    print(response) # Python

# 2. Functional programming
# Functional programming is a programming paradigm that treats computation as the evaluation of mathematical
#  functions and avoids changing-state and mutable data.

import functools
func_result = functools.reduce(lambda x, y: x + y, characters)
print()
print(func_result) # Python

# 3. Procedural programming
# Procedural programming is a programming paradigm that uses procedures (functions) to operate on data structures.
def stringify(characters):
    result = ''
    for character in characters:
        result += character
    return result

print(stringify(characters)) # Python

# 4. Object-oriented programming
# Object-oriented programming is a programming paradigm that uses objects to design applications and computer programs.

class Stringify:
    def __init__(self, characters):
        self.characters = characters

    def stringify(self):
        self.string = ''.join(self.characters)


sample_string = Stringify(characters)
sample_string.stringify()
print(sample_string.string) # Python
