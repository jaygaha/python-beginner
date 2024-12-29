# keyword argument = An argument preceded by an identifier
# helps with readability
# order of argument doesn't mater
# 1. positional, 2. default, 3. keyword, 4. arbitrary

# keyword

def hello(greeting, title, first_name, last_name):
    print(f"{greeting} {title} {first_name} {last_name}")

hello("Hello", last_name="Doe", title="Mr.", first_name="John")



def get_phone(country_code, area_code, first, last):
    return f"{country_code}-{area_code}-{first}-{last}"

phone_num = get_phone(country_code=81, first=9841, last=4421, area_code=80)

print(phone_num)