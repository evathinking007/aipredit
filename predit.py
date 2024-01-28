import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 加载数据
file_path = 'bitcoin_data_with_indicators2.xlsx'  # 更改为您的文件路径
bitcoin_data = pd.read_excel(file_path)

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

# 使用模型进行未来价格预测
# 提取最后一个时间点的特征数据
last_features = bitcoin_data[[ 'Volume','MA']].iloc[0].values



# 预测未来10个价格值
future_prices = []
for _ in range(1):
    future_price = model.predict([last_features])[0]
    future_prices.append(future_price)
    # 更新特征数据，将新的预测值添加到特征数据的末尾
    last_features = np.append(last_features[1:], [future_price])

print("未来1个价格预测:")
print(future_prices)
