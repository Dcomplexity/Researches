import numpy as np
np.random.seed(0)
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
import os

abspath = os.path.abspath(os.path.join(os.getcwd(), "../"))
dirname = abspath + "/New_Value_From_-3_To_3/One_Dimension_GroupSize_2/"
for root, dirs, files in os.walk(dirname):
    for filename in files:
        print (filename)
    if ".DS_Store" in files:
        files.remove(".DS_Store")
    files.sort()
print (files)

picFilename = []
for i in range(4):
    picFilename.append(dirname + files[i]) # The file name list
fPic = []
for i in range(4):
    fPic.append(open(picFilename[i]))

data = [[] for i in range(4)]
for i in range(4):
    for line in fPic[i].readlines():
        sigLine = []
        for num in line.strip().split('\t'):
            sigLine.append(float(num))
        data[i].append(sigLine)

npData = []
for i in range(4):
    npData.append(np.array(data[i]))
picData = [np.zeros((7, 7)) for i in range(4)]
for i in range(4):
    for ii in range(picData[i].shape[0]):
        for jj in range(picData[i].shape[1]):
            picData[i][ii][jj] = npData[i][ii*7+jj][2]
    picData[i] = picData[i].T

plt.figure(figsize=(12, 20))
plt.subplot(2, 2, 1)
plt.title("b=0.9")
xlabel = range(-3, 4)
ylabel = range(-3, 4)
ax = sns.heatmap(picData[0], cmap="YlGnBu", center = 0.5)
ax.set_xticklabels(xlabel)
ax.set_yticklabels(ylabel)
plt.ylabel("Update_Distance_Param " + r"$\beta$")

plt.subplot(2, 2, 2)
plt.title("b=1.0")
xlabel = range(-3, 4)
ylabel = range(-3, 4)
ax = sns.heatmap(picData[1], cmap="YlGnBu", center=0.5)
ax.set_xticklabels(xlabel)
ax.set_yticklabels(ylabel)

plt.subplot(2, 2, 3)
plt.title("b=1.1")
xlabel = range(-3, 4)
ylabel = range(-3, 4)
ax = sns.heatmap(picData[2], cmap="YlGnBu", center=0.5)
ax.set_xticklabels(xlabel)
ax.set_yticklabels(ylabel)
plt.xlabel("Interaction_Distance_Param " + r"$\alpha$")
plt.ylabel("Update_Distance_Param " + r"$\beta$")

plt.subplot(2, 2, 4)
plt.title("b=1.2")
xlabel = range(-3, 4)
ylabel = range(-3, 4)
ax = sns.heatmap(picData[3], cmap="YlGnBu", center=0.5)
ax.set_xticklabels(xlabel)
ax.set_yticklabels(ylabel)
plt.xlabel("Interaction_Distance_Param " + r"$\alpha$")
plt.show()