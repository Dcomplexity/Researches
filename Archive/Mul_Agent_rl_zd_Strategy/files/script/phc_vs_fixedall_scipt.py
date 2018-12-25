import string
import numpy as np
from matplotlib import pyplot as plt


# 这里如果把文件存储成二进制文件，是不是就好处理多了
file = open("../results/phc_vs_fixedall.txt")

data = file.readlines()
for line in data:
    line.strip()

file.close()

data_dict = {}
keys = []
values = []
for i in range(len(data)):
    if i % 5 == 0:
        keysList =  []
        keysTemp = data[i].strip().split(",")
        for j in keysTemp:
            keysList.append(float(j))
    if i % 5 == 1:
        strTemp = ''
        valuesDict = {}
        valuesTemp = data[i].strip()
        strTemp = valuesTemp.replace('array([', '', 4)
        strTemp = strTemp.replace('])', '', 4)
        strTemp = strTemp.replace('{(0, 0): ', '')
        strTemp = strTemp.replace('(0, 1): ', '')
        strTemp = strTemp.replace('(1, 0): ', '')
        strTemp = strTemp.replace('(1, 1): ', '')
        strTemp = strTemp.replace('}', '')
        strTemp = strTemp.strip(' ').split(',')
        valuesDict[(0, 0)] = (float(strTemp[0]), float(strTemp[1]))
        valuesDict[(0, 1)] = (float(strTemp[2]), float(strTemp[3]))
        valuesDict[(1, 0)] = (float(strTemp[4]), float(strTemp[5]))
        valuesDict[(1, 1)] = (float(strTemp[6]), float(strTemp[7]))

    if i % 5 == 1:
        data_dict[tuple(keysList)] = valuesDict

extortionStrategy = []
for keys1 in data_dict.keys():
    flag = 1
    for keys2 in data_dict[keys1].keys():
        if data_dict[keys1][keys2] != (0.0, 1.0):
            flag = 0
            break
    if flag == 1:
        extortionStrategy.append(keys1) 

stra0 = []
stra1 = []
stra2 = []
stra3 = []
for item in extortionStrategy:
    stra0.append(item[0])
    stra1.append(item[1])
    stra2.append(item[2])
    stra3.append(item[3])

mean0 = np.mean(stra0)
mean1 = np.mean(stra1)
mean2 = np.mean(stra2)
mean3 = np.mean(stra3)

# standard deviation
std0 = np.std(stra0)
std1 = np.std(stra1)
std2 = np.std(stra2)
std3 = np.std(stra3)

plt.errorbar([1,2,3,4], [mean0, mean1, mean2, mean3], yerr=[std0, std1, std2, std3], fmt='-o')
plt.show()

# itemFre = [0.0, 0.0, 0.0, 0.0]
# itemCount = 0.0
# for item in extortionStrategy:
#     itemCount += 1.0
#     itemFre[0] += item[0]
#     itemFre[1] += item[1]
#     itemFre[2] += item[2]
#     itemFre[3] += item[3]

# for i in range(len(itemFre)):
#     itemFre[i] = itemFre[i] / itemCount

# print (itemFre)           
