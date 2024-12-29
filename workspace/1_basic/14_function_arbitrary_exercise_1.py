def shipping_label(*args, **kwargs):
    for arg in args:
        print(arg, end=" ")
    print()

    # for key, value in kwargs.items():
    #     print(f"{key}: {value}")
    if "apartment" in kwargs:
        print(f"{kwargs.get('apartment')}")
    print(f"{kwargs.get('street')}")
    print(f"{kwargs.get('city')} {kwargs.get('zip')}")

shipping_label("Mr.", "John", "Doe", "II",
               street="132 fake st.",
               city="Tokyo",
               zip="136-0001",
               apartment="Apaman II")

print()

shipping_label("Mrs.", "Johna", "Doe", "II",
               street="987 fake st.",
               city="Osaka",
               zip="321-0001")