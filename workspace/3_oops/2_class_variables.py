# class variables = shared among all instances of a class
# Defined outside the constructor
# Allows to share data among all objects created from that class

class Student:
    # class variables
    class_year = 2024
    num_students = 0

    def __init__(self, name, age, grade):
        # instance variables
        self.name = name
        self.age = age
        self.grade = grade

        Student.num_students += 1

student1 = Student("Naruto", 17, 11)
student2 = Student("Sato", 16, 11)
student3 = Student("Kita", 17, 11)

print (student1.name)
print (student2.age)

# good to access directly from the class itself, if it is accessed via method it will ambigious
# print (student1.class_year)
print (Student.class_year)

print(Student.num_students) # 3

print()
print(f"My graduating class of {Student.class_year} has {Student.num_students} students")
print (student1.name)
print (student2.name)
print (student3.name)