import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
import os




tab=[]
x=[]
E=30000
for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-x"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-x", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.0.pickle', '')
        x.append(int(chan))
        tab.append(file.flux)


plt.plot(x, tab, '.')
Rd = np.arange(-150., 150, 0.2)


plt.show()