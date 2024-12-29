# Python quiz game

questions = ("What is the capital of Japan?",
             "What is the most abudant gas in Earth's atmosphere?",
             "How many nucleotides are there in DNA?",
             "What is 3 * 3?")

options = (("A: Tokyo", "B: Beijing", "C: Seoul", "D: Kathmandu"),
            ("A: Oxygen", "B: Nitrogen", "C: Carbon Dioxide", "D: Argon"),
            ("A: 3", "B: 4", "C: 5", "D: 6"),
            ("A: 6", "B: 9", "C: 12", "D: 15"))

answers = ("A", "B", "D", "B")
guesses = []
score = 0
question_number = 0

for question in questions:
    print("--------------------")
    print(question)
    for option in options[question_number]:
        print(option)

    guess = input("Enter your answer (A,B,C,D): ").upper()
    guesses.append(guess)
    if (guess == answers[question_number]):
        score += 1
        print("Correct!")
    else:
        print("Wrong!")
        print(f"The correct answer is {answers[question_number]}")

    question_number += 1

print("--------------------")
print("Quiz Results")
print("--------------------")

print ("Your answers: ", end="")
for answer in answers:
    print(answer, end=" ")
print()


print ("Your gueses: ", end="")
for guess in guesses:
    print(guess, end=" ")
print()

score = int(score / len(questions) * 100)
print(f"Your score is {score}%")
print("--------------------")