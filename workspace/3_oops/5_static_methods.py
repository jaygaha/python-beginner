# Static methods: A method that belong to a class rather than any object from that class (instance)
#   Usually used for general utility functions
#
#   1. Instance method: Best for operations on instance of the class (objects)
#   2. Static method: Best for utility functions that do not need access to class data

class Employee:

    def __init__(self, name, position):
        self.name = name
        self.position = position

    # Instance method
    def get_info(self):
        return f"{self.name} = {self.position}"

    @staticmethod
    def is_valid_position(position):
        valid_positions = ["Manager", "Cashier", "Cook", "Janitor"]

        return position in valid_positions

print(Employee.is_valid_position("Cook")) # True
print(Employee.is_valid_position("Waiter")) # False
print()

emp1 = Employee("Harke", "Manager")
emp2 = Employee("Ratey", "Cashier")
emp3 = Employee("Putke", "Cook")

print(emp1.get_info())
print(emp2.get_info())
print(emp3.get_info())