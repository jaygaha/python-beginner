# TODO: Fix this string!
ford_quote = "Whether you think you can, or you think you can't--you're right."

username = "Yogesh"
timestamp = "16:20"
url = "http://petshop.com/pets/reptiles/pythons"

# TODO: print a log message using the variables above.
# The message should have the same format as this one:
# "Yogesh accessed the site http://petshop.com/pets/reptiles/pythons at 16:20."
message = username + " accessed the site " + url + " at " + timestamp + "."
print(message)

# LEN
given_name = "William"
middle_names = "Bradley"
family_name = "Pitt"

full_name = given_name + " " + middle_names + " " + family_name
name_length = len(full_name)

# name_length = len(given_name + middle_names + family_name) + 2. The +2 accounts for the spaces in between each word.

# Now we check to make sure that the name fits within the driving license character limit
# Nothing you need to do here
driving_license_character_limit = 28
print(name_length <= driving_license_character_limit)

# print(len(835)) # error len only works on sequences, not numbers
