class Category:
    def __init__(self, name: str):
        self.name = name
        self.total_funds = 0.0
        self.ledger = []

    def __str__(self):
        title = f'{self.name.center(30, '*')}\n'
        body = [ f'{entry.description.ljust(23)}' + f'{f'{entry.amount:.2f}'.rjust(7)}\n' \
            for entry in self.ledger ]

        return f'{title}{''.join(body)}Total: {self.total_funds:.2f}'

    def deposit(self, amount: float, description=''):
        if amount <= 0:
            raise ValueError('Amount should be positive.')

        self.ledger.append(LedgerEntry(amount, description))
        self.total_funds += amount
    
    def withdraw(self, amount: float, description: str=''):
        if amount <= 0:
            raise ValueError('Amount should be positive.')
        
        if not self.check_funds(amount):
            return False
        else:
            self.ledger.append(LedgerEntry(-amount, description))
            self.total_funds -= amount
            return True

    def get_balance(self):
        return self.total_funds

    def transfer(self, amount: float, category):
        if amount <= 0:
            raise ValueError('Amount should be positive.')

        if not self.check_funds(amount):
            return False
        
        self.withdraw(amount, f'Transfer to {category.name}')
        category.deposit(amount, f'Transfer from {self.name}')

        return True

    def check_funds(self, amount: float):
        return amount < self.total_funds
        
class LedgerEntry:
    def __init__(self, amount: float, description: str=''):
        self.amount = amount
        self.description = description
        self.type = 'Deposit' if amount > 0 else 'Withdrawal'

    def __str__(self):
        return f'Description: {self.description}, Amount: {self.amount}, Type: {self.type}'

def get_category_expenses(category):
    return -sum([ expense.amount for expense in category.ledger if expense.type == 'Withdrawal' ])

def create_spend_chart(categories):
    total_expenses = sum ([ get_category_expenses(category) for category in categories ])
    percentual_expenses = { category.name : get_category_expenses(category) \
        for category in categories }

if __name__ == '__main__':
    print('Some tests:')
    game_wallet = Category('Games')
    game_wallet.deposit(10, 'Games expense reservation')
    game_wallet.withdraw(2, 'Tabletop RPG supplies')

    food_wallet = Category('Food')
    food_wallet.deposit(15, 'Food expense reservation')
    food_wallet.withdraw(3, 'Banana')
    food_wallet.withdraw(2, 'Apple')
    food_wallet.transfer(1, game_wallet)

    print('Ledger:', [ str(entry) for entry in food_wallet.ledger ])
    print('Expenses', get_category_expenses(food_wallet))


    print('Category format test')
    print(food_wallet)
    print(game_wallet)

    wallets = [ food_wallet, game_wallet ]