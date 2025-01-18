# Practice Question

# Question: Create a function that opens the flowers.txt, reads every line in it, and saves it as a dictionary.
# The main (separate) function should take user input (user's first name and last name) and parse the user input to identify the first letter of the first name.
# It should then use it to print the flower name with the same first letter (from dictionary created in the first function).
# Sample Output:

# >>> Enter your First [space] Last name only: Bill Newman
# >>> Unique flower name with the first letter: Bellflower


# Answer

# Create a function that opens the flowers.txt, reads every line in it, and saves it as a dictionary.

def create_flower_dict(filename):
    # flower_dict = {}

    # with open(filename, "r") as f:
    #     for line in f:
    #         line = line.strip()
    #         flower_dict[line[0]] = line

    # return flower_dict
    """Load flower names from a file and return a dictionary."""
    flowers_dict = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                flower_name = line.strip()
                if flower_name:  # Ensure the line is not empty
                    first_letter = flower_name[0].upper()  # Use uppercase for consistency
                    if first_letter not in flowers_dict:
                        flowers_dict[first_letter] = []
                    flowers_dict[first_letter].append(flower_name)
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
    return flowers_dict


# The main (separate) function should take user input (user's first name and last name) and parse the user input to identify the first letter of the first name.

# def main():
#     flower_dict = create_flower_dict("workspace/50_udacity/6_scripts/quiz/flowers.txt")
#     first_name = input("Enter your First [space] Last name only?: ").split(" ")

#     first_letter = first_name[0].lower()
#     # print(flower_dict[first_letter])
#     print(flower_dict, first_letter)

def get_flower_by_first_name(flowers_dict):
    """Get a flower name based on the first letter of the user's first name."""
    user_input = input("Enter your First [space] Last name only: ")
    first_name = user_input.split()[0]  # Get the first name
    first_letter = first_name[0].upper()  # Get the first letter and convert to uppercase

    if first_letter in flowers_dict:
        flower_name = flowers_dict[first_letter][0]  # Get the first flower name for that letter
        # A: African Daisy, B: Bellflower
        # Get only the flower name remove A: or B:
        flower_name = flower_name.split(": ")[1]
        print(f"Unique flower name with the first letter: {flower_name}")
    else:
        print(f"No flower name found for the letter '{first_letter}'.")



def main():
    flowers_dict = create_flower_dict("workspace/50_udacity/6_scripts/quiz/flowers.txt")
    get_flower_by_first_name(flowers_dict)

if __name__ == "__main__":
    main()


# Alternative Answer
## function that creates a flower_dictionary from filename
def create_flowerdict(filename):
    flower_dict = {}
    with open(filename) as f:
        for line in f:
            letter = line.split(": ")[0].lower()
            flower = line.split(": ")[1].strip()
            flower_dict[letter] = flower
    return flower_dict

## Main function that prompts for user input, parses out the first letter
## includes function call for create_flowerdict to create dictionary
def main1():
    flower_d = create_flowerdict('workspace/50_udacity/6_scripts/quiz/flowers.txt')
    full_name = input("Enter your First [space] Last name only: ")
    first_name = full_name[0].lower()
    first_letter = first_name[0]
    ## print command that prints final input with value from corresponding key in dictionary
    print("Unique flower name with the first letter: {}".format(flower_d[first_letter]))

main1()