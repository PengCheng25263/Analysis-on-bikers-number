import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from stats import skewness

# pretreatment
bikes = pd.read_csv('C:\\Users\\Think\\Desktop\\6200\\challenge Q\\bikes.csv', header=7)
df0 = bikes.drop(columns=["Female", "No", "No.1", "No.2"])
df1 = df0.fillna(0)
df1.columns = ['datetime', 'gender', 'had_helmet', 'had_passenger', 'on_sidewalk']

# problem 1
a = '7:00'
m = 0
for i in df1['datetime']:
    if i == 0:
        df1.iloc[m, 0] = "2010--9-24 " + a
    else:
        a = i
        df1.iloc[m, 0] = "2010--9-24 " + i
    m += 1
df1["gender"].replace("X", 'Male', inplace=True)
df1["gender"].replace(0, 'Female', inplace=True)
df1.replace(0, "No", inplace=True)
df1.replace("X", "Yes", inplace=True)
df1["datetime"] = pd.to_datetime(df1["datetime"])
print(df1)
# df1.to_csv('out.csv')

# problem 2
df2 = df1.describe(include="all")
print(df2)
# df2.to_csv("out2.csv")

# problem 3
df3 = df1.groupby(by=["datetime", "gender"])
df4 = df3.size().unstack()
df4 = df4.fillna(0)
# print(df4)
datetime_list = df4.index
Male_number = df4["Male"]
Female_number = df4["Female"]
plt.bar(range(len(Male_number)), Male_number, label='male', fc='y')
plt.bar(range(len(Female_number)), Female_number, bottom=Male_number, label='female', tick_label=datetime_list, fc='g')
plt.legend()
plt.xlabel("datetime")
plt.ylabel("count")
plt.xticks(np.arange(8, 48, 12), ("09:00", "12:00", "15:00", "18:00"))
plt.show()

# problem 4
plt.bar(range(len(Female_number)), Female_number, label='Female', fc='b')
plt.legend()
plt.xlabel("datetime")
plt.ylabel("count")
plt.show()
Min = min(Female_number)
print("min =", Min)
Max = max(Female_number)
print("max =", Max)
Mean = np.mean(Female_number)
print("mean =", Mean)
Median = np.median(Female_number)
print("median =", Median)
Variance = np.var(Female_number, ddof=1)
print("variance =", Variance)
Std = np.std(Female_number, ddof=1)
print("std =", Std)
Cov = Std/Mean
print("cov =", Cov)
Lexis = Variance/Mean
print("Lexis =", Lexis)
Skewness = skewness(Female_number)
print("Skewness =", Skewness)
