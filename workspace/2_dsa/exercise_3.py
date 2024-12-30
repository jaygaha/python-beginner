# Encryption program
# Subsitution cyper program

import random
import string

chars = " " + string.punctuation + string.digits + string.ascii_letters

chars = list(chars)
key = chars.copy()

random.shuffle(key)

# print(f"chars: {chars}")
# print(f"key: {key}")

# Encrypt
plain_text = input("Enter your message: ")
ciper_text = ""

for letter in plain_text:
    index = chars.index(letter)
    ciper_text += key[index]

print(f"Original message: {plain_text}")
print(f"Encrypted message: {ciper_text}")

# Decrypt
ciper_text = input("Enter your encrypted message: ")
plain_text = ""

for letter in ciper_text:
    index = key.index(letter)
    plain_text += chars[index]

print(f"Encrypted message: {ciper_text}")
print(f"Original message: {plain_text}")