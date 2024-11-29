import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x ** 2)

fig, ax = plt.subplots()
ax.plot(x, y, label='A long label that takes up too much space')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 6})
plt.show()