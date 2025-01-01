# Class method: Allowing access to the class from the instance
#   Take (cls/self) as the first argument, which represents the class itself
#
# Instance method: Best for operations on instance of the class (object)
# Static method: Best for utility functions, which do not require access to the class or instance
# Class method: Best for class-level operations, which require access to the class, but not the instance

class Employee:

    num_of_emps = 0
    total_pay = 0

    def __init__(self, name, pay):
        self.name = name
        self.pay = pay
        self.email = name + '@company.com'
        Employee.num_of_emps += 1
        Employee.total_pay += pay

    # Instance method
    def get_info(self):
        return (f"{self.name}: {self.pay}")

    @classmethod
    def get_num_of_emps(cls):
        return (f"Total # of employees: {cls.num_of_emps}")

    @classmethod
    def get_avg_pay(cls):
        if cls.num_of_emps == 0:
            return 0

        return f"Average pay: {cls.total_pay / cls.num_of_emps:0.2f}"

emp1 = Employee('Doe', 6000)
emp2 = Employee('John', 5000)
emp3 = Employee('Jane', 7000)

print(Employee.get_num_of_emps())
print(Employee.get_avg_pay())