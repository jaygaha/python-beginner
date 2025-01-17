# Files
# 1 Reading from a file
#
f = open("workspace/50_udacity/6_scripts/quiz/file.txt", "r")
file_data = f.read()
f.close()

print(file_data)

# 2 Writing to a file

f = open("workspace/50_udacity/6_scripts/quiz/file1.txt", "w")
f.write(file_data)
f.close()

# with: no need to close the file
with open("workspace/50_udacity/6_scripts/quiz/file.txt", "r") as f:
    file_data1 = f.read()

print(file_data1)

# Read method with an integer argument
with open("workspace/50_udacity/6_scripts/quiz/file.txt", "r") as f:
    print(f.read(2))
    print(f.read(8))


# readline: reads a single line from the file
with open("workspace/50_udacity/6_scripts/quiz/file1.txt", "r") as f:
    print(f.readline())

print()

# with for loop
file_lines = []
with open("workspace/50_udacity/6_scripts/quiz/file1.txt", "r") as f:
    for line in f:
        file_lines.append(line.strip())

print(file_lines)

print()
# Quiz: Flying Circus Cast List
def create_cast_list(filename):
    cast_list = []
    #use with to open the file filename
    with open(filename, "r") as f:
        #use the for loop syntax to process each line
        for line in f:
            #strip the line of whitespace
            line = line.split(",")[0]

            #and add the actor name to cast_list
            cast_list.append(line)

    return cast_list

cast_list = create_cast_list('workspace/50_udacity/6_scripts/quiz/flying_circus_cast.txt')
for actor in cast_list:
    print(actor)


# User input numlists
# initiate empty list to hold user input and sum value of zero
user_list = []
list_sum = 0

# seek user input for ten numbers
for i in range(10):
    userInput = input("{}. Enter any 2-digit number: ".format(i + 1))

    # check to see if number is even and if yes, add to list_sum
    # print incorrect value warning  when ValueError exception occurs
    try:
        number = int(userInput)
        user_list.append(number)
        if number % 2 == 0:
            list_sum += number
    except ValueError:
        print("Incorrect value. That's not an int!")

print("user_list: {}".format(user_list))
print("The sum of the even numbers in user_list is: {}.".format(list_sum))

print()
# Too many files open
files = []

# for i in range(10000):
#     files.append(open("workspace/50_udacity/6_scripts/quiz/file.txt", "r"))
#     print(i)
