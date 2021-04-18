import matplotlib.pyplot as plt

with open('data.txt', 'r') as f:
    data = [float(i) for i in f.read().split()]

plt.plot(data, label='brightness')
plt.xlabel('time')
plt.ylabel('% britness')
plt.show()
