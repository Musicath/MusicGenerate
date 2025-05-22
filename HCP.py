from scipy.optimize import minimize
from scipy.optimize import Bounds
from musicpy import *
from tool import *
import numpy as np
import pickle
import os
import random
import math
import time

start = time.time()
songs = []

for i in os.listdir('song'):
    file = open('song' + os.sep + i, 'rb')
    song = pickle.load(file)
    file.close()
    songs.append(song)

songs = Tune_Init(songs)
fun = lambda hnn: -ASRHCP(songs, 3, hnn)  # 设置最优化函数
bounds = Bounds([1] * 12, [1000] * 12)  # 边界条件
cons = ({'type': 'eq', 'fun': lambda hnn: Norm(hnn, 3) - 1000})  # 约束条件
h0 = [random.random() * 999 + 1 for i in range(12)]  # 迭代初始值
res = minimize(fun, h0, method='SLSQP', bounds=bounds, constraints=cons)  # 求解
#####
print('最小值：', res.fun)
print('最优解：', res.x)
print('是否顺利进行：', res.success)
print('迭代终止原因：', res.message)

s = 0
x = np.zeros(12)
for i in range(12):
    s += res.x[i]
s = s
for i in range(12):
    x[i] = res.x[i] / s
file = open('HarmonyLambda.pkl', 'wb')
pickle.dump(x, file)
file.close()
print(x)
print("运行时间：", time.time() - start)
