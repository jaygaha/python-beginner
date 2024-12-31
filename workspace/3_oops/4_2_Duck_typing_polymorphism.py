# "Duck typing": Another way to achieve polymorphism besides Inheritance
#   Object must have the minimum necessary attributes/methods
#   "If it looks like a duck and quacks like a duck, it must be a duck"

# 2. Duck Typing

class Animal:
    is_alive = True

class Dog(Animal):
    def speak(self):
        print("Bhaw Bhaw!!")

class Cat(Animal):
    def speak(self):
        print("Meow!!")

class Car:
    is_alive = False

    def speak(self):
        print("Peep peep!!!")

animals = [Dog(), Cat(), Car()]

for animal in animals:
    animal.speak()
    print(animal.is_alive)