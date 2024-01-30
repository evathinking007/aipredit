class Contract:
    def __init__(self, initial_balance=10000):
        self.balance = initial_balance
        self.grid_size = 1000
        
    def buy_contract(self, amount, price):
        cost = amount * price
        if cost > self.balance:
            print("Insufficient balance to buy the contract.")
        else:
            self.balance -= cost
            print(f"Bought {amount} contracts for ${cost}")
    
    def sell_contract(self, amount, price):
        sale = amount * price
        self.balance += sale
        print(f"Sold {amount} contracts for ${sale}")
    
    def apply_grid_trading(self, current_price):
        lower_price = int(current_price / self.grid_size) * self.grid_size
        upper_price = lower_price + self.grid_size
        
        self.buy_contract(1, lower_price)
        self.sell_contract(1, upper_price)
    
    def get_balance(self):
        print(f"Current balance: ${self.balance}")


# Test the grid trading process
contract = Contract()

contract.buy_contract(5, 4500)  # Buy 5 contracts at $4500
contract.sell_contract(3, 4600)  # Sell 3 contracts at $4600

contract.apply_grid_trading(4700)  # Apply grid trading at $4700

contract.get_balance()  # Check the current balance
