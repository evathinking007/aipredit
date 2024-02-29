import warnings
import openpyxl
from datetime import timedelta
from datetime import datetime, timezone
import time
import requests
import logging
import threading
import math
import pandas as pd

def setup_logger(name, log_file, level=logging.INFO):
    # """Function to setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
class Strategy:
    def __init__(self,logger):
        self.logger = logger
        pass



class Exchange:
    def __init__(self, logger):
        self.logger = logger
        pass

    def GetAccount(self):
        pass

    def GetTicker(self):
        pass

    def Buy(self,price,position_percent,end_price):
        pass

    def Sell(self,price,position_percent,end_price):
        pass



# 判断盈利还是亏损函数，并返回盈利状态和盈利点数
def trade_liq_status(currentprice, order, marginlevel):
    money_point = 0
    trade_money_status = False
    trade_direction = "hold"
    # 如果订单type是0，则为买单，且offset为0开仓，则为做多
    if order.Type == 0 and order.Offset == 0:
        # 那么当前价格比订单价格高，则是盈利
        if currentprice > order.Price:
            trade_money_status = True
            money_point = (currentprice - order.Price) * marginlevel  # 则为盈利点数
            trade_direction = "buy"
        else:
            trade_money_status = False
            money_point = (currentprice - order.Price) * marginlevel  # 则为亏损点数
            trade_direction = "buy"
    # 如果订单type是1，则为卖单，且offset为0开仓，则为做空
    if order.Type == 1 and order.Offset == 0:
        # 那么当前价格比订单价格低，则是盈利
        if currentprice < order.Price:
            trade_money_status = True
            money_point = (order.Price - currentprice) * marginlevel  # 则为盈利点数
            trade_direction = "sell"
        else:
            trade_money_status = False
            money_point = (order.Price - currentprice) * marginlevel  # 则为亏损点数
            trade_direction = "sell"

    return trade_direction, trade_money_status, money_point


def round_down(value, decimals):
    factor = 10 ** decimals
    return math.floor(value * factor) / factor


def get_right_time(self, minutes_to_add):
    # 获取当前时间
    current_time = datetime.now()
    # 计算下一个整点时刻
    next_time = current_time + timedelta(minutes=minutes_to_add)
    next_time = next_time.replace(second=0)

    # 计算等待时间，直到下一个整点时刻
    time_to_wait = (next_time - current_time).total_seconds()
    self.logger.info(f"等待到下一个整点时刻（{next_time.strftime('%d/%m/%Y, %H:%M:%S')}）")
    time.sleep(time_to_wait)

def calculate_fee(quantity, price, fee_rate):
    """
    计算数字货币合约交易手续费的函数

    :param quantity: 交易数量
    :param price: 交易价格
    :param fee_rate: 手续费率
    :return: 手续费
    """
    fee = quantity * price * fee_rate
    return fee


def main():
    # 创建日志把手
    coin_name="ETH"
    log_file_name = f"{coin_name}USDT_execute.log"
    logger = setup_logger(coin_name, log_file_name)

    exchange=Exchange(logger)
    marginlevel = 100
    closepoint = 200
    backpoint = closepoint
    # 定义一个下单的id，每次交易一个跟踪id，开仓有orderid，平仓有closeid
    orderid = None
    closeid = None
    atr_bz = 15
    wait_min = 5 * 60 * 1000
    exchange.SetContractType("swap")

    closeprice = 0  # 平仓价格

    while True:
        # 待定是否需要交易信号
        # 得到5min历史数据
        # 计算ma
        # 判断交易信号，如果是三线出现信号，且有一定的分开比例，则入，


        # 同时给出做空或者做多的两个方向的单，
        # 同时设置各自的止损位为3个价格波动
        # 循环查看交易单是否成交，如果成交则开始跟单，否则循环睡眠1min
        # 得到单1和单2id
        # 每隔1min获取两个合约的收益变化，如果收益之和为正，记录一个最大max收益
            # 直到其中1个止损平仓
            # 如果最大max收益回撤20%且收益-手续费大于10U，则一键平全部仓
            # 手续费计算(quantity, current_price, fee_rate))
        # 循环查看2个交易单是否平仓完毕，否则循环睡眠1min
        # sleep5min，等下一个交易信号


        # 获取账户
        account = exchange.GetAccount()
        # Log(account)
        ticker=exchange.GetTicker()

        currentprice = float(records[-1]["Close"])

        # 获取信号
        # signal = judge_bs_point(atr, atr_bz, records)

        # 得到可以买的量
        amount = round_down(float(account["Stocks"]) * float(marginlevel) / currentprice, 2)

        # Log(account["Stocks"],amount,signal,currentprice,atr[-1])

        # 下单交易
        if orderid is None:
            max_money_point = 0  # 最大盈利点
            max_money_price = 0  # 暂时没有用，可能有用，暂时保留该值
            closeprice = 0  # 平仓价格
            if signal == "buy":
                exchange.SetMarginLevel(marginlevel)
                exchange.SetDirection("buy")
                orderid = exchange.Buy(currentprice, amount)
            elif signal == "sell":
                exchange.SetMarginLevel(marginlevel)
                exchange.SetDirection("sell")
                orderid = exchange.Sell(currentprice, amount)
            else:
                Sleep(wait_min)
                continue  # 则没有入场点，进入下一个循环

        # // 参数id为订单号码，需填入你想要查询的订单的号码,Type:0是buy，1是sell，Offset：0代表开仓，1代表平仓
        else:
            order = exchange.GetOrder(orderid)
            Log("开仓:", "Id:", order.Id, "Price:", order.Price, "Amount:", order.Amount, "DealAmount:",
                order.DealAmount, "Status:", order.Status, "Type:", order.Type, "Offset：", order.Offset)
            # # 如果订单已经被平仓了，则需要重新把orderid置空，进入下一轮买卖
            if order.Offset == 1:
                orderid = None
                closeid = None
                Sleep(wait_min)
                continue
                # if order.Status ==0:
            #     Sleep(wait_min)
            #     continue
            # 等待成交
            if order.Status != 1:
                Sleep(5 * 60 * 1000)
                continue

                # 成交后打印订单信息
                # Log("Id:", order.Id, "Price:", order.Price, "Amount:", order.Amount, "DealAmount:",
                #     order.DealAmount, "Status:", order.Status, "Type:", order.Type,"Offset：",order.Offset)

            trade_direction, trade_money_status, money_point = trade_liq_status(currentprice, order, marginlevel)
            Log(trade_direction, trade_money_status, money_point)

            # 如果当前价格比起订单价格在盈利状态，则启用动态止损规则：
            if trade_money_status:

                # 先取消以前的止损订单
                # if closeid is not None:
                #     exchange.CancelOrder(closeid)

                # 如果是做多，则动态止损平仓价是当前价格-止损点
                if trade_direction == "buy":
                    closeprice = currentprice - closepoint / marginlevel
                # 如果是做空，则动态止损平仓价是当前价格+止损点
                if trade_direction == "sell":
                    closeprice = currentprice + closepoint / marginlevel
                Log(closeprice, "动态止损", currentprice)

                # 如果当前盈利点数大于等于最大盈利点数，说明此时利润还是增长，不止盈，没有平仓价，同时更新盈利的点数最大值
                if money_point >= max_money_point:
                    max_money_point = money_point
                    max_money_price = currentprice  # 暂时没有用，可能有用，暂时保留该值
                    Log("最大盈利点是:", max_money_point)
                    Sleep(wait_min)
                    continue  # 跳出此次循环继续进入下一个价格判断
                # 如果当前盈利点数小于最大盈利点数，说明在回撤了，当达到预设最大回撤值时，则平仓，没达到预设最大回撤值，则循环
                elif money_point < max_money_point:
                    if max_money_point - money_point >= backpoint:
                        if trade_direction == "buy":
                            exchange.SetMarginLevel(marginlevel)
                            exchange.SetDirection("closebuy")
                            # amount = exchange.GetPosition()[0].Amount   # 首先获取持仓
                            amount = order.Amount
                            closeid = exchange.Sell(-1, amount)
                            closeorder = exchange.GetOrder(closeid)
                            Log("平仓：", "Id:", closeorder.Id, "Price:", closeorder.Price, "Amount:", closeorder.Amount,
                                "DealAmount:",
                                closeorder.DealAmount, "Status:", closeorder.Status, "Type:", closeorder.Type,
                                "Offset：", closeorder.Offset)
                            orderid = None
                        if trade_direction == "sell":
                            exchange.SetMarginLevel(marginlevel)
                            exchange.SetDirection("closesell")
                            # amount = exchange.GetPosition()[0].Amount   # 首先获取持仓
                            amount = order.Amount
                            closeid = exchange.Buy(-1, amount)
                            closeorder = exchange.GetOrder(closeid)
                            Log("平仓：", "Id:", closeorder.Id, "Price:", closeorder.Price, "Amount:", closeorder.Amount,
                                "DealAmount:",
                                closeorder.DealAmount, "Status:", closeorder.Status, "Type:", closeorder.Type,
                                "Offset：", closeorder.Offset)
                            orderid = None
                    else:
                        Sleep(wait_min)
                        continue
                Log("盈利", closeprice, money_point, max_money_point, currentprice)

            # 如果当前价格比起订单价格在亏损状态，则直接止损点平仓，代表开仓方向错了：
            else:
                # 如果是做多，则closeprice是订单价格-止损点
                if trade_direction == "buy":
                    closeprice = order.Price - closepoint / marginlevel
                    # 如果是做空，则closeprice是订单价格+止损点
                if trade_direction == "sell":
                    closeprice = order.Price + closepoint / marginlevel
                Log(closeprice, "亏损", currentprice)

            # 如果是做多，且当前价格比止损价格还低，则止损平仓
            if trade_direction == "buy":
                if currentprice <= closeprice:
                    exchange.SetMarginLevel(marginlevel)
                    exchange.SetDirection("closebuy")
                    # amount = exchange.GetPosition()[0].Amount   # 首先获取持仓
                    amount = order.Amount
                    closeid = exchange.Sell(-1, amount)
                    closeorder = exchange.GetOrder(closeid)
                    Log("平仓：", "Id:", closeorder.Id, "Price:", closeorder.Price, "Amount:", closeorder.Amount,
                        "DealAmount:",
                        closeorder.DealAmount, "Status:", closeorder.Status, "Type:", closeorder.Type, "Offset：",
                        closeorder.Offset)
                    orderid = None
                else:
                    Sleep(wait_min)
                    continue
            # 如果是做空，且当前价格比止损价格还高，则止损平仓
            if trade_direction == "sell":
                if currentprice >= closeprice:
                    exchange.SetMarginLevel(marginlevel)
                    exchange.SetDirection("closesell")
                    # amount = exchange.GetPosition()[0].Amount   # 首先获取持仓
                    amount = order.Amount
                    closeid = exchange.Buy(-1, amount)
                    closeorder = exchange.GetOrder(closeid)
                    Log("平仓：", "Id:", closeorder.Id, "Price:", closeorder.Price, "Amount:", closeorder.Amount,
                        "DealAmount:",
                        closeorder.DealAmount, "Status:", closeorder.Status, "Type:", closeorder.Type, "Offset：",
                        closeorder.Offset)
                    orderid = None
                else:
                    Sleep(wait_min)
                    continue

        Sleep(wait_min)

