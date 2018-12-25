import pylab

def readfile(filename):
    f = open(filename)
    data = f.readlines()
    f.close()
    return data

data = readfile('rewardSumList1.txt')
rewardSumListFull = []
for item in data:
    rewardSumListFull.append(float(item.strip()))
rewardSumList = rewardSumListFull[0: 400000]
pylab.figure()
pylab.title('Rewards with time (Only Learn)')
pylab.xlabel('TimeStep')
pylab.ylabel('Rewards')
pylab.plot(rewardSumList, 'k')
pylab.show()
