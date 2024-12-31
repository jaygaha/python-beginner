# Inheritance: allows one class to inherit the properties and behavior of another class.
# Helps with code reusability and extensibility
# class Chind(Parent)

class Animal:
    def __init__(self, name):
        self.name = name
        self.is_alive = True

    def eat(self):
        print(f"{self.name} is eating")

    def sleep(self):
        print(f"{self.name} is sleeping")


class Dog(Animal):
    def speak(self):
        print("Bhaw Bhaw!!")

class Cat(Animal):
    def speak(self):
        print("Meow!!")

class Mouse(Animal):
    def speak(self):
        print("chi chi!!")

dog = Dog("Kukur")
cat = Cat("Biralo")
mouse = Mouse("musa")

print(dog.name)
print(dog.is_alive)

# dog.eat()
# dog.sleep()

# print(mouse.name)
# print(cat.is_alive)

# cat.eat()
# mouse.sleep()

dog.speak()
cat.speak()
mouse.speak()


# print(dog.name)