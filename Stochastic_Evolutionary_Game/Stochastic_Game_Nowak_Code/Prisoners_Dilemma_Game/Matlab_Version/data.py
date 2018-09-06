import pylab
import scipy.io as scio

data = scio.loadmat('Coop_Time')

coopS = data['ans'][0]
coop1 = data['ans'][1]
coop2 = data['ans'][2]

pylab.figure()
pylab.title('Cooperation Rate with Time')
pylab.xlabel('Time')
pylab.ylabel('Cooperation Fraction')
pylab.plot(coopS, 'k')
pylab.plot(coop1, 'r')
pylab.plot(coop2, 'g')
pylab.show()
