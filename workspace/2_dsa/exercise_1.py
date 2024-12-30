# Python banking program

def show_balace(balance):
    print("***************************")
    print(f"Your balance total is ${balance:.2f}")
    print("***************************")

def deposit():
    print("***************************")
    amount = float(input("Enter amount to be deposited: "))
    print("***************************")

    if (amount < 0):
        print("***************************")
        print("Please provide valid amount")
        print("***************************")
        return 0
    else:
        return amount


def withdraw(balance):
    print("***************************")
    amount = float(input("Enter amount to be withdrawn: "))
    print("***************************")

    if amount > balance:
        print("***************************")
        print("Insufficient balance")
        print("***************************")
        return 0
    elif amount < 0:
        print("***************************")
        print("Amount must be greater than 0")
        print("***************************")
        return 0
    else:
        return amount

def main():
    balance= 0
    is_running = True

    while is_running:
        print("***************************")
        print("Banking Program")
        print("***************************")
        print("1. Show Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")
        print("***************************")

        choice = input("Enter the option (1-4): ")

        if choice == "1":
            show_balace(balance)
        elif choice == "2":
            balance += deposit()
        elif choice == "3":
            balance -= withdraw(balance)
        elif choice == "4":
            is_running = False
        else:
            print("***************************")
            print("Invalid choice")
            print("***************************")
    print("***************************")
    print("Thank you!")
    print("***************************")


if __name__ == "__main__":
    main()