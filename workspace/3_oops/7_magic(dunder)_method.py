# Magic methods: dunder/double underscore methods
# __init__, __str__, __eq__
# These methods are called automatically when certain operations are performed on objects.
# Allow developers to define custom behavior for objects.

class Book:

    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        return (f"'{self.title}' by {self.author}")

    def __eq__(self, other):
        return self.title == other.title and self.author == other.author

    def __lt__(self, other):
        return self.pages < other.pages

    def __gt__(self, other):
        return self.pages > other.pages

    def __add__(self, other):
        return f"{self.pages + other.pages} pages"

    def __contains__(self, keyword):
        return keyword in self.title or keyword in self.author

    def __getitem__(self, key):
        if key == 'title':
            return self.title
        elif key == 'author':
            return self.author
        elif key == 'pages':
            return self.pages
        else:
            return f"Invalid key: {key}"

book1 = Book('Python', 'John Doe', 210)
book2 = Book('Python', 'John Doe', 210)
# book2 = Book('Java', 'Jane Doe', 330)
book3 = Book('PHP', 'Hacker', 192)

# __str__ method is called automatically when we print the object instead memory address is printed.
print(book1)
print(book2)
print(book3)

# __eq__ method is called automatically when we compare two objects.
print(book1 == book2)
print(book2 < book3)
print(book2 > book3)
print(book2 + book3)

print("PHP" in book3)
print("John" in book1)

print(book1['title'])
print(book1['audio'])