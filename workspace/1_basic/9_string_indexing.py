#  String indexing: accessing elements of a sequence using their index
# [start:stop:step]

credit_card = "1234-5678-9012-3456"

print(credit_card[0])  # 1

print(credit_card[5])  # 5

print(credit_card[0:4])  # 1234
print(credit_card[:4])  # 1234

print(credit_card[5:9])  # 5678
print(credit_card[5:])  # 5678-9012-3456

print(credit_card[-1])  # 6
print(credit_card[-4:])  # 3456

print(credit_card[::2])  # 13-6891-46
print(credit_card[::3])  # 14-79-5

last_digits = credit_card[-4:] # 3456

print(f"XXXX-XXXX-XXXX-{last_digits}")  # XXXX-XXXX-XXXX-3456

credit_card = credit_card[::-1] # reverse the string

print(credit_card)  # 6543-2109-8765-4321


