import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import random
import matplotlib.pyplot as plt
from datetime import timedelta
from datetime import datetime
import re
import time
import requests
def caculate_data(file_path):
    df = pd.read_excel(file_path)
    ma_period = 20  # 移动平均的周期
    if not pd.isna(df.at[0, "MA"]):
        return
    df['MA'] = df['Price'].rolling(window=ma_period).mean()

    # 计算相对强弱指标（RSI）
    rsi_period = 14  # RSI的周期
    price_diff = df['Price'].diff()
    gain = price_diff.where(price_diff > 0, 0)
    loss = -price_diff.where(price_diff < 0, 0)
    avg_gain = gain.rolling(window=rsi_period).mean()
    avg_loss = loss.rolling(window=rsi_period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    df['RSI'] = rsi

    # 计算布林带的上限（Upper_BB）和下限（Lower_BB）
    bb_period = 20  # 布林带的周期
    std_dev = df['Price'].rolling(window=bb_period).std()
    df['Upper_BB'] = df['MA'] + (2 * std_dev)
    df['Lower_BB'] = df['MA'] - (2 * std_dev)
    df = df.iloc[20:]
    new_column_name = 'Future_Price'
    df[new_column_name] =None
    # 回写到Excel文件
    df['Date'] = df['Date'].str.replace('UTC+0', '')

    df.to_excel(file_path, index=False)

def train_data(bitcoin_data):


    # 选择特征和目标变量
    #features = bitcoin_data[['Volume', 'MA', 'RSI', 'Upper_BB', 'Lower_BB']]
    features = bitcoin_data[[ 'Volume','MA']]
    target = bitcoin_data['Price']

    # 划分数据集为训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # 创建并拟合线性回归模型
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 预测测试集的价格
    y_pred = model.predict(X_test)
    # print(y_pred)
    # 评估模型性能
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"均方误差 (MSE): {mse}")
    print(f"决定系数 (R^2): {r2}")
    return model

def predict_next(model,bitcoin_data):
    # 使用模型进行未来价格预测
    last_feature = bitcoin_data[[ 'Volume','MA']].iloc[-1].values
    future_price = model.predict([last_feature]) 
    return future_price
    
def write_next_data(pd,future_price):
    new_datetime = pd.to_datetime(bitcoin_data['Date'].iloc[-1])

    # 增加1小时
    new_datetime = new_datetime + timedelta(hours=1)
    new_data = {
    'Date':new_datetime,  # 示例时间
    'Price': None,  # 示例价格
    'Volume': None, # 示例成交量
    'MA':None,
    'RSI':None,
    'Upper_BB':None,
    'Lower_BB':None,
    'Future_Price':future_price,
    }

    bitcoin_data = pd.concat([bitcoin_data, pd.DataFrame(new_data)], ignore_index=True)
    # 回写到Excel文件
    bitcoin_data.to_excel(file_path, index=False)

def test_history(model,bitcoin_data,start,lengthrecord):
    # 数据回测
    for i in range(start,start+lengthrecord):
        #random_integer = random.randint(2, 1000)    
        random_integer=i
        # 提取最后一个时间点的特征数据
        last_feature = bitcoin_data[[ 'Volume','MA']].iloc[-random_integer].values
        current_price=bitcoin_data[['Price']].iloc[-random_integer+1].values
        future_price = model.predict([last_feature]) 
        # # bitcoin_data.loc[-random_integer+1, "Future_Price"]= future_price
        # bitcoin_data["Future_Price"][-random_integer+1] = future_price
        bitcoin_data['Future_Price'].iloc[-random_integer+1]= future_price
        # 回写到Excel文件
        bitcoin_data.to_excel(file_path, index=False)

def get_data_api(bitcoin_data):

    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/spot/candlesticks'
    query_param = 'currency_pair=BTC_USDT&limit=1'
    while True:
        r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
        print(r.json()) 
        get_right_time(minutes_to_add)
        # data_k_date= datetime.utcfromtimestamp(int(r.json()[0][0])).strftime('%Y-%m-%d %H:%M:%S')
        data_k_date=datetime.now()
        data_k_price=r.json()[0][2]
        data_k_volume=r.json()[0][6]
        new_data = {
        'Date':[data_k_date],  # 示例时间
        'Price': [data_k_price],  # 示例价格
        'Volume': [data_k_volume], # 示例成交量
        'MA':[None],
        'RSI':[None],
        'Upper_BB':[None],
        'Lower_BB':[None],
        'Future_Price':[None],
        }
        print(new_data)
        bitcoin_data = pd.concat([bitcoin_data, pd.DataFrame(new_data)], ignore_index=True)
        bitcoin_data.to_excel(file_path, index=False)

def get_right_time(minutes_to_add):
    # 获取当前时间
    current_time = datetime.now()
    # 计算下一个整点时刻
    next_time = current_time + timedelta(minutes=minutes_to_add)
    next_time = next_time.replace(second=0)

    # 计算等待时间，直到下一个整点时刻
    time_to_wait = (next_time - current_time).total_seconds()
    print(f"等待到下一个整点时刻（{next_time.strftime('%d/%m/%Y, %H:%M:%S')}）")
    time.sleep(time_to_wait)

if __name__ == "__main__":
    # 加载数据
    file_path = 'bitcoin_data.xlsx'  # 更改为您的文件路径
   # caculate_data(file_path) # 计算均值等技术指标
    bitcoin_data = pd.read_excel(file_path)
    #model=train_data(bitcoin_data) # 训练模型
    #furture_price=predict_next(model,bitcoin_data) # 预测下一个未来值
    #print(furture_price)
    minutes_to_add=1

    while True:
        
        get_data_api(bitcoin_data)

    
    
    # 目的一是运行一段时间看下预测情况
        
    #     每隔1分钟抓取一次，写入数据库表

    #     然后回测一条数据，得到该时间的预测值
    #       test_history(model,bitcoin_data,2,1)
        
    #     运行7天，查看最终的预测情况

    # 目的二是模拟一个账户进行买卖看下收益情况
    #     如果是上涨，则在当前价格买入，

   # test_history(model,bitcoin_data,1,100)# 回测数据,起始为1的话，代表全部回测
   

