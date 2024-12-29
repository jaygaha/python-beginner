# match-case statement: (switch) an alternative to using many `elif` statements
#   Execute some code if a value matches a `case`
#   Cleaner and readble syntax

def day_of_week(day):
    match day:
        case 1:
            return "It's Sunday"
        case 2:
            return "It's Monday"
        case 3:
            return "It's Tuesday"
        case 4:
            return "It's Wednesday"
        case 5:
            return "It's Thursday"
        case 6:
            return "It's Friday"
        case 7:
            return "It's Saturday"
        case _:
            return "Not a valid day"

print(day_of_week(1))


# OR |
def is_weekend(day):
    match day:
        case "Sunday" | "Saturday":
            return True
        case "Monday" | "Tuesday"  | "Wednesday" | "Thursday" | "Friday":
            return False
        case _:
            return False

print(is_weekend("Monday")) # False
print(is_weekend("Saturday")) # True
print(is_weekend("today")) # False
