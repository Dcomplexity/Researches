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

picFilename = dirname + files[3]
fPic = open(picFilename)
data = []
for line in fPic.readlines():
    sigLine = []
    for num in line.strip().split('\t'):
        sigLine.append(float(num))
    data.append(sigLine)
print (data)

npData = np.array(data)
picData = np.zeros((7, 7))
for i in range(picData.shape[0]):
    for j in range(picData.shape[1]):
        picData[i][j] = npData[i * 7 + j][2]
picData = picData.T
print (picData)
xlabel = range(-3, 4)
ylabel = range(-3, 4)
ax = sns.heatmap(picData, cmap="YlGnBu")
ax.set_xticklabels(xlabel)
ax.set_yticklabels(ylabel)
plt.xlabel("Interaction_Distance_Param " + r"$\alpha$")
plt.ylabel("Update_Distance_Param " + r"$\beta$")
plt.show()
