import pylab

def readfile(filename):
    f = open(filename)
    data = f.readlines()
    f.close()
    return data

data = readfile('rewardSumList1.txt')
rewardSumList = []
for item in data:
    rewardSumList.append(float(item.strip()))
pylab.figure()
pylab.title('Rewards with time')
pylab.xlabel('TimeStep')
pylab.ylabel('Rewards')
pylab.plot(rewardSumList, 'k')
pylab.show()
