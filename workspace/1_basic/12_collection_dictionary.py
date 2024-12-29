# Dictionary: a collection which is unordered, changeable and indexed. No duplicate members.
# {key:value, key:value, key:value} pair

capitals = {"Nepal":"Kathmandu",
            "USA":"Washington DC",
            "UK":"London",
            "Japan":"Tokyo",
            "China":"Beijing"}

# print(dir(capitals))
# print(help(capitals))

print(capitals.get("Nepal")) # Kathmandu

# unknow country
print(capitals.get("India")) # None

# if condition
if capitals.get("Japan"):
    print("That capital exists")
else:
    print("That capital does not exists")

# update value: add or update
capitals.update({"Nepal":"Pokhara"})
capitals.update({"Bhutan":"Timphu"})

print(capitals) # {'Nepal': 'Pokhara', 'USA': 'Washington DC', 'UK': 'London', 'Japan': 'Tokyo', 'China': 'Beijing', 'Bhutan': 'Timphu'}

# revert back to original
capitals["Nepal"] = "Kathmandu"

# remove item
capitals.pop("UK")

print(capitals) # {'Nepal': 'Kathmandu', 'USA': 'Washington DC', 'Japan': 'Tokyo', 'China': 'Beijing', 'Bhutan': 'Timphu'}

# popitem: remove last item
capitals.popitem()

print(capitals) # {'Nepal': 'Kathmandu', 'USA': 'Washington DC', 'Japan': 'Tokyo', 'China': 'Beijing'}

# get keys
country_keys = capitals.keys()
print(country_keys) # dict_keys(['Nepal', 'USA', 'Japan', 'China'])

for key in country_keys:
    print(key)

# get values
country_values = capitals.values()

print(country_values) # dict_values(['Kathmandu', 'Washington DC', 'Tokyo', 'Beijing'])

for value in country_values:
    print(value)

# get items
country_items = capitals.items()

print(country_items) # dict_items([('Nepal', 'Kathmandu'), ('USA', 'Washington DC'), ('Japan', 'Tokyo'), ('China', 'Beijing')])

for key, item in country_items:
    print(f"{key}: {item}")