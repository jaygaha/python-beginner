# Rock, Paper, Scissors game

import random

options = ("rock", "paper", "scissors")
is_playing = True

while is_playing:
    player = None
    computer = random.choice(options)

    while player not in options:
        player = input("Enter a choice (rock, paper, scissors): ").lower()

    print(f"Player: {player}")
    print(f"Computer: {computer}")

    if (player == computer):
        print("Oh! it's a tie!")
    elif player == "rock" and computer == "scissors":
        print("You win!")
    elif player == "paper" and computer == "rock":
        print("You win!")
    elif player == "scissors" and computer == "paper":
        print("You win!")
    else:
        print("You lose!")

    if not input("Play again? (y/n):").lower() == "y":
        is_playing = False


print("Thanks for playing!")

