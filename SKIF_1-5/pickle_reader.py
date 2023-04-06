import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
import os




tabx=[]
taby=[]
tabz=[]
x=[]
y=[]
z=[]
E=30000
for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-z"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-z", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.0.pickle', '')
        z.append(int(chan))
        tabz.append(g.flux)


plt.plot(z, tabz, '.')
plt.show()
for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-x"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-x", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.0.pickle', '')
        x.append(int(chan))
        tabx.append(g.flux)


plt.plot(x, tabx, '.')
plt.show()
for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-y"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-y", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.0.pickle', '')
        y.append(int(chan))
        taby.append(g.flux)


plt.plot(y, taby, '.')

plt.show()