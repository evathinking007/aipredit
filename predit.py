import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout

# 加载数据
file_path = 'bitcoin_data_with_indicators.xlsx'  # 更改为你的文件路径
bitcoin_data = pd.read_excel(file_path)

# 数据预处理
# 删除含有NaN的行
bitcoin_data = bitcoin_data.dropna()

# 选择目标变量（价格）和技术指标作为特征
target_column = 'Price'
#features = bitcoin_data[['Price', 'MA', 'RSI', 'Upper_BB', 'Lower_BB']].values
features = bitcoin_data[['Price']].values
# 归一化特征数据#
scaler_features = MinMaxScaler(feature_range=(0, 1))
scaled_features = scaler_features.fit_transform(features)

# 创建时间序列数据集
def create_dataset(data, time_step=1):
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), :])
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)

# 使用60个时间步长来预测下一个时间点
time_step = 1000
X, y = create_dataset(scaled_features, time_step)

# 重塑输入以适应LSTM网络
X = X.reshape(X.shape[0], X.shape[1], X.shape[2])

# 划分数据集为训练集和测试集
train_size = int(len(X) * 0.80)
X_train, X_test = X[0:train_size, :], X[train_size:len(X), :]
y_train, y_test = y[0:train_size], y[train_size:len(y)]

# 构建LSTM模型
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, X.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(25))
model.add(Dense(1))

# 编译模型
model.compile(optimizer='adam', loss='mean_squared_error')

# 训练模型
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=64, verbose=1)

# 预测未来价格的函数
def predict_next_hours(model, features_data, time_step, future_hours=10):
    last_data = features_data[-time_step:]
    predicted_prices = []
    for _ in range(future_hours):
        last_data_scaled = scaler_features.transform(last_data)
        last_data_scaled = last_data_scaled.reshape(1, time_step, last_data.shape[1])
        predicted_price_scaled = model.predict(last_data_scaled)[0, 0]
        #last_data = np.append(last_data[1:], [[predicted_price_scaled] + last_data[-1, 1:]], axis=0)
        new_row = np.insert(last_data[-1, 1:], 0, predicted_price_scaled)
        last_data = np.append(last_data[1:], [new_row], axis=0)

        predicted_price = scaler_features.inverse_transform(last_data_scaled[0, -1, :].reshape(1, -1))[0, 0]
        predicted_prices.append(predicted_price)
    return predicted_prices

# 预测未来10小时的价格
predicted_prices = predict_next_hours(model, scaled_features, time_step, 10)
print(predicted_prices)
