# Multilevel inheitance: inherit from a parent which inherits from another parent
# C(B) <- B(A) <- A

# Parent class
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating")

    def sleep(self):
        print(f"{self.name} is sleeping")

# Child class
class Prey(Animal):
    def flee(self):
        print(f"{self.name} is fleeing")

class Predator(Animal):
    def hunt(self):
        print(f"{self.name} is hunting")


class Rabbit(Prey):
    pass

class Hawk(Predator):
    pass

class Fish(Prey, Predator):
    pass

rabbit = Rabbit("Kharayo")
hawk = Hawk("Chil")
fish = Fish("Maccha")

rabbit.eat()

hawk.sleep()

print()
fish.eat()
fish.sleep()