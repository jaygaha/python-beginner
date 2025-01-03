# Hash Table (Hashmap): It is a type of data structure that maps keys to its value pairs.
# It is implemented through the built-in data type: dictinary

glossary = {"BCP": "Business Continuity Plan"}
print(glossary) # {'BCP': 'Business Continuity Plan'}

# add
glossary['GIL'] = "Gloabl Inter Lock"
print(glossary) # {'BCP': 'Business Continuity Plan', 'GIL': 'Gloabl Inter Lock'}

# update
glossary['GIL'] = "Gloabl Interpreter Lock"
print(glossary) # {'BCP': 'Business Continuity Plan', 'GIL': 'Gloabl Interpreter Lock'}

#search
print(glossary["BCP"]) # Business Continuity Plan

# delete
del glossary["BCP"]
print(glossary) # {'GIL': 'Gloabl Interpreter Lock'}

print(type(glossary)) # <class 'dict'>


# Hash function: it perform hashing by turning any data into a fixed-size sequence of bytes call the hash value or the hash code.
# its a number that can act as a digital fingerprint or a digest.

print(hash(3.14159)) # 326484311674566659

# Compare an Object’s Identity With Its Hash
# id(): returns a fixed-size integer in a deterministic way.

print(id('Lorem')) # 1425855460768