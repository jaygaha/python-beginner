# Python Slot Machine Program
import random

def spin_row():
    symbols = ['🍒','🍉','🍋','🔔','⭐']

    # results = []
    # for symbol in range(3):
    #     results.append(random.choice(symbols))

    # return results

    # List compreshension
    return [random.choice(symbols) for _ in range(3)]


def print_row(row):
    print("***************")
    print(" | ".join(row))
    print("***************")

def get_payout(row, bet):
    if row[0] == row[1] == row[2]:
        if row[0] == '🍒':
            return bet * 3
        elif row[0] == '🍉':
            return bet * 4
        elif row[0] == '🍋':
            return bet * 5
        elif row[0] == '🔔':
            return bet * 10
        elif row[0] == '⭐':
            return bet * 20

    return 0

def main():
    print("##########################")
    print("Welcome to Python Slots")
    print("Symbols: 🍒🍉🍋🔔⭐")
    print("##########################")
    print()
    balance = int(input("How much money do you want to deposit to play? $"))

    while balance > 0:
        print(f"Current balance: ${balance}")

        bet = input("Place your bet amount: $")

        if not bet.isdigit():
            print("Please enter a valid amount")
            continue

        bet = int(bet)

        if bet > balance:
            print("Insufficient funds")
            continue

        if bet <= 0:
            print("Bet must be greater than 0")
            continue

        balance -= bet

        row = spin_row()
        print()
        print("Spinning...\n")
        print_row(row)

        payout = get_payout(row, bet)

        if (payout > 0):
            print(f"You WON ${payout}")
        else:
            print("Sorry you lost this round.")

        balance += payout

        play_again = input("Do you want to spin again? (Y/N)").upper()

        if (play_again != 'Y'):
            break

    print()
    print("********************************************")
    print(f"Game over! Your final balance is ${balance}")
    print("********************************************")


if __name__ == '__main__':
    main()