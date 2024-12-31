# multiple inheritance = inherit from more than one parent class
# C(A, B)

# Parent class
class Prey:
    def flee(self):
        print("This animal is fleeing")

class Predator:
    def hunt(self):
        print("This animal is hunting")

# Child class
class Rabbit(Prey):
    pass

class Hawk(Predator):
    pass

class Fish(Prey, Predator):
    pass

rabbit = Rabbit()
hawk = Hawk()
fish = Fish()

rabbit.flee()

hawk.hunt()

print()
fish.flee()
fish.hunt()
