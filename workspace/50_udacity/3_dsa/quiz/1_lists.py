# Types of Data Structures: Lists, Tuples, Sets, Dictionaries, Compound Data Structures
# Operators: Membership, Identity
# Built-In Functions or Methods
#
# 1. Lists: a data type for mutable ordered sequences of items
# 2. Tuples: a data type for immutable ordered sequences of items
# 3. Sets: a data type for unordered collections of unique items
# 4. Dictionaries: a data type for unordered collections of key-value pairs
# 5. Compound Data Structures: a data type for combining multiple data type

month = 8
days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31]

# use list indexing to determine the number of days in month
num_days = days_in_month[month - 1]
print(num_days)


eclipse_dates = ['June 21, 2001', 'December 4, 2002', 'November 23, 2003',
                 'March 29, 2006', 'August 1, 2008', 'July 22, 2009',
                 'July 11, 2010', 'November 13, 2012', 'March 20, 2015',
                 'March 9, 2016']


# TODO: Modify this line so it prints the last three elements of the list
eclipse_dates = eclipse_dates[-3:]
print(eclipse_dates)

sentence1 = "I wish to register a complaint."
sentence2 = ["I", "wish", "to", "register", "a", "complaint", "."]
sentence2[6]="!"
print(sentence2)

# sentence1[30] = '!' # TypeError: string indices must be integers

sentence2[0:2] = ["We", "want"]
print(sentence2)
