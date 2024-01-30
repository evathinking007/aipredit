class Contract:
    def __init__(self, initial_balance=10000):
        self.balance = initial_balance

    def execute_trade(self, action, quantity, price):
        cost = quantity * price
        if action == "buy" and cost <= self.balance:
            self.balance -= cost
            print(f"Bought {quantity} contracts at price {price} for ${cost}")
        elif action == "sell":
            self.balance += cost
            print(f"Sold {quantity} contracts at price {price} for ${cost}")
        else:
            print("Insufficient balance to buy the contract.")

    def get_balance(self):
        print(f"Current balance: ${self.balance}")


# 使用实时价格进行期货交易
def maximize_profit(prediction, price):
    contract = Contract()

    if prediction > price:
        # 如果预测价格为上涨，则买入期货合约
        contract.execute_trade("buy", 10, price)
    else:
        # 如果预测价格为下跌，则卖出期货合约
        contract.execute_trade("sell", 10, price)

    contract.get_balance()  # 查询当前余额


# 测试
# 假设预测值为110，当前价格为100
maximize_profit(110, 105)  # 假设实时价格为105
