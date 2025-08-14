class Category:
    def __init__(self, name):
        self.name = name
        self.total_funds = 0.0
        self.ledger = []

    def deposit(self, amount, description=''):
        if amount <= 0:
            raise ValueError('Amount should be positive.')

        self.ledger.append({amount, description})
        self.total_funds += amount
    
    def withdraw(self, amount, description=''):
        if amount <= 0:
            raise ValueError('Amount should be positive.')
        
        if self.total_funds < amount:
            return False
        else:
            self.ledger.append({-amount, description})
            self.total_funds -= amount

def create_spend_chart(categories):
    pass

if __name__ == '__main__':
    print('Some tests:')
    
    cat = Category('Food')
    cat.deposit(5, 'bananas')
    cat.deposit(7)
    cat.deposit(2, 'bananas')
    cat.withdraw(3, 'withdraw')

    print('Ledger:', cat.ledger)
    print('Total funds:', cat.total_funds)