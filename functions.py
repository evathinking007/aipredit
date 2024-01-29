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

def test_history(model,bitcoin_data,record):
    # 数据回测
    for i in range(2,record):
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


if __name__ == "__main__":
    # 加载数据
    file_path = 'bitcoin_data.xlsx'  # 更改为您的文件路径
    caculate_data(file_path) # 计算均值等技术指标
    bitcoin_data = pd.read_excel(file_path)
    model=train_data(bitcoin_data) # 训练模型
    furture_price=predict_next(model,bitcoin_data) # 预测下一个未来值
    print(furture_price)

    如果是上涨，则在当前价格买入，
    实现数据抓取，并写入数据库中
    目的一是运行一段时间看下预测情况
    目的二是模拟一个账户进行买卖看下收益情况

   # test_history(model,bitcoin_data,100)# 回测数据
   

