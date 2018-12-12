import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sympy import *
from scipy.optimize import fsolve
from scipy.special import beta


# pretreatment
# bikes = pd.read_csv('C:\\Users\\Think\\Desktop\\6200\\challenge Q\\bikes.csv', header=7)
bikes = pd.read_csv('bikes.csv', header=7)
df0 = bikes.drop(columns=["Female", "No", "No.1", "No.2"])
df1 = df0.fillna(0)
df1.columns = ['datetime', 'gender', 'had_helmet', 'had_passenger', 'on_sidewalk']

# problem 1
a = '7:00'
m = 0
for i in df1['datetime']:
    if i == 0:
        df1.iloc[m, 0] = "2010-9-24 " + a
    else:
        a = i
        df1.iloc[m, 0] = "2010-9-24 " + i
    m += 1
df1["gender"].replace("X", 'Male', inplace=True)
df1["gender"].replace(0, 'Female', inplace=True)
df1.replace(0, "No", inplace=True)
df1.replace("X", "Yes", inplace=True)
df1["datetime"] = pd.to_datetime(df1["datetime"])
print(df1)
df1.to_csv('out.csv')

# problem 2
df2 = df1.describe(include="all")
print(df2)
df2.to_csv("out2.csv")

# problem 3
df3 = df1.groupby(by=["datetime", "gender"])
df4 = df3.size().unstack()
df4 = df4.fillna(0)
print(df4)
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
print(Female_number)
m = np.sum(Female_number)
print("m = ", m)
Female_pdf = Female_number.apply(lambda x: x / m)
print(Female_pdf)
new_index = np.arange(1.00, 49.00)
counter = 0
for index in range(len(new_index)):
    new_index[counter] = new_index[counter] / 48
    counter += 1
print(new_index)

# another way to calculate mean
# Female_mean = []
# i = 0
# for index in range(len(Female_pdf)):
#     Female_mean.append(Female_pdf[i] * new_index[i])
#     i += 1
# Mean = np.sum(Female_mean)

Mean = 0
i = 0
for index in range(len(Female_pdf)):
    Mean = Mean + new_index[i] * Female_pdf[i]
    i += 1
print("Mean= ", Mean)

Mean_2 = 0
i = 0
for index in range(len(Female_pdf)):
    Mean_2 = Mean_2 + (new_index[i]**2) * Female_pdf[i]
    i += 1
print("Mean_2= ", Mean_2)

Female_variance = Female_pdf
print("new_index=", new_index)
print("Female_pfd=", Female_pdf)
print("Mean=", Mean)

j = 0
Variance = 0
for index in range(len(new_index)):
    Variance = Variance + np.square(new_index[j] - Mean) * Female_pdf[j]
    j += 1
Variance = np.sum(Female_variance)
print("Var =", Variance)
print("new_index[0]=", new_index[0])


Std = np.sqrt(Variance)
Cov = Std / Mean
print("cov =", Cov)
Lexis = Variance / Mean
print("Lexis =", Lexis)


Ske = 0
k = 0
for index in range(len(Female_pdf)):
    Ske = Ske + pow(new_index[k] - Mean, 3)/48
    k += 1
print(Ske)
Skewness = Ske / pow(Variance, 1.5)
print("Skewness =", Skewness)


def f(a1):
    x = float(a1[0])
    y = float(a1[1])
    return [
        x/(x+y),
        (x * y)/(np.square(x + y) * (x + y + 1))+x**2/((x+y)**2)
    ]


a0 = [Mean, Mean_2]
result = fsolve(f, a0)
print(result)
# print(result[0], result[1])


def b(x):
    float(x)
    return (1/beta(result[0], result[1]))*(x**(result[0]-1))*((1-x)**(result[1]-1))


i = 10
chi = 0
while i <= 40:
    chi = chi + (Female_number[i]**2)/(861*b(new_index[i]))
    i += 1
chi = chi - 861
print("chi teat result =", chi)

if chi > 65:
    print("the chi-test is not passed")
else:
    print("the chi-test is passed")

