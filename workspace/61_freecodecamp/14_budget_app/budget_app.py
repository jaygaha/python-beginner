# Budget App
# https://www.freecodecamp.org/learn/scientific-computing-with-python/build-a-budget-app-project/build-a-budget-app-project
#

class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        else:
            return False

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {category.name}')
            category.deposit(amount, f'Transfer from {self.name}')
            return True
        else:
            return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = f'{self.name:*^30}\n'
        items = ''
        for item in self.ledger:
            amount = f"{item['amount']:7.2f}"
            description = item['description'][:23]
            items += f'{description:<23}{amount:>7}\n'
        total = f'Total: {self.get_balance():.2f}'
        return title + items + total

def create_spend_chart(categories):
    category_withdrawals = {}

    # Calculate withdrawals for each category
    for category in categories:
        withdrawals = 0
        for transaction in category.ledger:
            amount = transaction['amount']
            if amount < 0:
                withdrawals += -amount  # Add the amount spent (negative for withdrawals)
        category_withdrawals[category.name] = withdrawals

    # Calculate total withdrawals across all categories
    total_withdrawals = sum(category_withdrawals.values())

    # Calculate percentages spent for each category based on withdrawals
    category_percentages = {}
    for name, withdrawals in category_withdrawals.items():
        category_percentages[name] = (withdrawals / total_withdrawals) * 100 if total_withdrawals > 0 else 0

    # Generate the chart body
    chart_str = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        line = f"{i:3}| "
        for name in category_percentages:
            percent = category_percentages[name]
            if percent >= i:
                line += "o  "
            else:
                line += "   "
        chart_str += line + "\n"

    # Print the horizontal line at the bottom of the chart
    chart_str += "    " + "-" * (len(category_percentages) * 3 + 1) + "\n"

    # Print category names vertically
    max_name_length = max(len(name) for name in category_percentages)
    for i in range(max_name_length):
        line = "     "
        for name in category_percentages:
            if i < len(name):
                line += name[i] + "  "
            else:
                line += "   "
        chart_str += line + "\n"

    return chart_str.rstrip("\n")


food = Category('Food')
food.deposit(1000, 'deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
food.transfer(50, clothing)
print(food)
print()

food1 = Category('Food')
entertainment = Category("Entertainment")
business = Category("Business")

food1.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)
actual = create_spend_chart([business, food1, entertainment])
print(actual)
