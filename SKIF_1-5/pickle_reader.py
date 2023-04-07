import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
import array as arr
from scipy.optimize import curve_fit
import math

tabx=[]
taby=[]
tabz=[]
tabpitch=[]
x=[]
y=[]
z=[]
pitch=arr.array('f',[])

def func_G(x,  b, c):
    return 1/(c*(2*np.pi)**0.5) * np.exp(-(x-b)**2 / 2*c**2)

def func_P(x, l, k):
    return l**k / math.factorial(k) * np.exp(-l)

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
popt, pcov = curve_fit(func_G, x, tabx)
plt.plot(x, func_G(x, *popt), 'r-')
for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-y"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-y", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.0.pickle', '')
        y.append(int(chan))
        taby.append(g.flux)

sp = plt.subplot(223)
plt.plot(y, taby, '.')
popt, pcov = curve_fit(func_G, y, taby)
plt.plot(y, func_G(y, *popt), 'r-')

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