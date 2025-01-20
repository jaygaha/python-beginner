# String
#
# Key aspects of variable naming in Python are:

#     Some words are reserved keywords (e.g. for, while, True). They have a special meaning in Python, so you cannot use them for variable names.
#     Variable names cannot start with a number, and they can only contain alpha-numeric characters or underscores.
#     Variable names are case sensitive, i.e. my_var is different from my_Var and MY_VAR.
#     Finally, it is a common convention to write variable names using snake_case, where each space is replaced by an underscore character and the words are written in lowercase letters.

# find(): nd the position in the string where the first occurrence of a substring is found
#
# Caesar cipher
# The first kind of cipher you are going to build is called a Caesar cipher. Specifically, you will take each letter in your message, find its position in the alphabet,
# take the letter located after 3 positions in the alphabet, and replace the original letter with the new letter.

# To implement this, you will use the .find() method discussed in the previous step. Modify your existing .find() call passing it text[0] as the argument instead of 'z'.
#
text = 'Hello Zaira'
shift = 3

def caesar(message, offset):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    encrypted_text = ''

    for char in message.lower():
        if char == ' ':
            encrypted_text += char
        else:
            index = alphabet.find(char)
            new_index = (index + offset) % len(alphabet)
            encrypted_text += alphabet[new_index]
    print('plain text:', message)
    print('encrypted text:', encrypted_text)

caesar(text, shift)
caesar(text, 13)

#############################################################
# Start transforming your Caesar cipher into a Vigenère cipher by removing the two function calls.
