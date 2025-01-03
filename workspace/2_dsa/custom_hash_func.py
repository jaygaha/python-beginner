# 7 Make Your Own Hash Function

def custom_hash_func(key):
    return sum(
        index * ord(character)
        for index, character in enumerate(repr(key).lstrip("'"), 1)
        )

# print(custom_hash_func('march 9')) # 12