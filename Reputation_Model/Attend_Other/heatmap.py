import numpy as np
np.random.seed(0)
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt

fStart = open('strategy_matrix_final.txt')
data = []
for line in fStart.readlines():
    sigLine = []
    for num in line.strip().split(' '):
        sigLine.append(float(num))
    data.append(sigLine)
npData = np.array(data)
print (npData)
# uniform_data = np.random.rand(10, 12)
ax = sns.heatmap(npData)
plt.show()