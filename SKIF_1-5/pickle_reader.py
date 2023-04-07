import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
import os
import array as arr



tabx=[]
taby=[]
tabz=[]
tabpitch=[]
x=[]
y=[]
z=[]
pitch=arr.array('f',[])


for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-z"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-z", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.0.pickle', '')
        z.append(int(chan))
        tabz.append(g.flux)

sp = plt.subplot(221)
plt.plot(z, tabz, '.')

for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-x"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-x", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.0.pickle', '')
        x.append(int(chan))
        tabx.append(g.flux)

sp = plt.subplot(222)
plt.plot(x, tabx, '.')

for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-y"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-y", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.0.pickle', '')
        y.append(int(chan))
        taby.append(g.flux)

sp = plt.subplot(223)
plt.plot(y, taby, '.')

for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-pitch"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-pitch", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.pickle', '')
        pitch.append(float(chan))
        tabpitch.append(g.flux)

sp = plt.subplot(224)
plt.plot(pitch, tabpitch, '.')
plt.show()