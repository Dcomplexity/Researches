import numpy as np
import matplotlib.pyplot as plt
import datetime

# In this work, 0 for cooperation and 1 for defection
p = [0.7881, 0.8888, 0.4686, 0.0792]
# p = [1.0, 1.0, 1.0, 1.0]
# p = [0.222, 0.111, 0.333, 0.0414]
q = [0.5, 0.5, 0.5, 0.5]
tm = [[p[0] * q[0], p[0] * (1 - q[0]), (1 - p[0]) * q[0], (1 - p[0]) * (1 - q[0])],
      [p[1] * q[2], p[1] * (1 - q[2]), (1 - p[1]) * q[2], (1 - p[1]) * (1 - q[2])],
      [p[2] * q[1], p[2] * (1 - q[1]), (1 - p[2]) * q[1], (1 - p[2]) * (1 - q[1])],
      [p[3] * q[3], p[3] * (1 - q[3]), (1 - p[3]) * q[3], (1 - p[3]) * (1 - q[3])]]
tm_m = np.matrix(tm)
v = [0.0, 1.0, 0.0, 0.0]
plot_data = []
# Two method time test
start_time = datetime.datetime.now()
for step in range(50):
      result = np.dot(v, np.linalg.matrix_power(tm, step))
      plot_data.append(np.array(result).flatten())
# result = v
# for step in range(2000):
#       plot_data.append(np.array(result).flatten())
#       result = np.dot(result, tm)
end_time = datetime.datetime.now()
print(end_time - start_time)
plot_data = np.array(plot_data)
print(plot_data)
plt.figure(1)
plt.xlabel('Steps')
plt.ylabel('Probability')
lines = []
for i, shape in zip(range(4), ['x', 'h', 'H', 's']):
      print(i)
      line, = plt.plot(plot_data[:, i], shape, label="S%i" %(i))
      lines.append(line)
plt.legend(handles=lines, loc=1)
plt.show()








