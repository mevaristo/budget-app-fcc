class Category:
    def __init__(self, name: str):
        self.name = name
        self.total_funds = 0.0
        self.expenses = 0.0
        self.ledger = []

    def __str__(self):
        title = f'{self.name.center(30, '*')}\n'
        body = [ f'{entry.description.ljust(23)[:23]}' + f'{f'{entry.amount:.2f}'.rjust(7)[0:7]}\n' \
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
            self.expenses += amount
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

    def __str__(self):
        return f'Description: {self.description}, Amount: {self.amount}'

def create_spend_chart(categories):
    total_expenses = sum ([ category.expenses for category in categories ])
    relative_percentual_expenses = { category.name : (100 * category.expenses) / total_expenses \
        for category in sorted(categories, key=lambda category: category.expenses, reverse=True) }
    spend_chart_column = create_spend_chart_percentage_columns()
    for key in relative_percentual_expenses:
        increment_spend_chart_column(int(relative_percentual_expenses[key]), spend_chart_column)

    return f'Percentage spent by category\n' + \
        str(relative_percentual_expenses) + \
        f'\n{verticalize_chart_percentage_column(spend_chart_column)}'

def create_spend_chart_percentage_columns():
    return { f'{_}': f'{_}|'.rjust(4) for _ in range(100, -1, -10) }

def increment_spend_chart_column(percentage: int, column: dict):
    for i, s in ((str(_), (' o ' if _ < percentage else '   ')) for _ in range(0, 101, 10)):
        column[i] = column[i] + s

def verticalize_chart_percentage_column(column: dict):
    return ''.join([ f'{column[key]}\n' for key in column ])

def create_spend_chart_label_columns():
    pass

        

if __name__ == '__main__':
    print('Some tests:')
    game_wallet = Category('Games')
    game_wallet.deposit(10, 'Games expense reservation')
    game_wallet.withdraw(2, 'Tabletop RPG supplies')

    food_wallet = Category('Food')
    food_wallet.deposit(15, 'Food expense reservation')
    food_wallet.withdraw(3, 'Banana')
    food_wallet.withdraw(2, 'Apple')
    food_wallet.withdraw(2, 'Pineapple')
    food_wallet.transfer(1, game_wallet)

    hardware_wallet = Category('Hardware')
    hardware_wallet.deposit(20, 'I\'m sure I will spend all this with hardware')
    hardware_wallet.withdraw(5, 'Buy a new tractor truck')
    hardware_wallet.withdraw(3, 'Buy a new truck')
    hardware_wallet.withdraw(3, 'Buy a hammer')

    print('Ledger:', [ str(entry) for entry in food_wallet.ledger ])
    print('Expenses', food_wallet.expenses)


    print('Category format test')
    wallets = [ food_wallet, game_wallet, hardware_wallet ]

    for wallet in wallets:
        print(wallet)

    print(create_spend_chart(wallets))
    