import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import random
import matplotlib.pyplot as plt
# 加载数据
file_path = 'bitcoin_data_with_indicators.xlsx'  # 更改为您的文件路径
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





# 预测未来10个价格值
deviation_rates = []
for _ in range(50):
    random_integer = random.randint(1, 1000)
    last_feature = bitcoin_data[[ 'Volume','MA']].iloc[random_integer].values
    current_price=bitcoin_data[['Price']].iloc[random_integer-1].values
    future_price = model.predict([last_feature]) 
    deviation_rate = abs(((current_price - future_price) / future_price) * 100)
    deviation_rates.append(deviation_rate[0])
    print("分析时间"+str(bitcoin_data[['Date']].iloc[random_integer].values))  
    print("未来价格预测:"+str(future_price))
    print("真实下一价格:"+str(current_price))
    print(f"偏差率为: {deviation_rate}%")
   

print(f"偏差率中的最大值是: {max(deviation_rates)}")
print(f"偏差率中的最小值是: {min(deviation_rates)}")
print(f"偏差率中的平均值是: {sum(deviation_rates) / len(deviation_rates)}")
# count_near_zero = sum(1 for value in deviation_rates if abs(value) < 0.05)
# percentage_near_zero = (count_near_zero / len(deviation_rates)) * 100
# print(f"接近0的数值的比例为: {percentage_near_zero}%")
# print(deviation_rates)
plt.hist(deviation_rates, bins=20, color='blue', alpha=0.7)
plt.xlabel('数值')
plt.ylabel('频率')
plt.title('数据的直方图')
plt.grid(True)
plt.show()
