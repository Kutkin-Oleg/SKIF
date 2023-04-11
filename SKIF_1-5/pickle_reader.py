import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
import array as arr
from scipy.optimize import curve_fit
import math


x=np.array([],dtype='f')
y=np.array([],dtype='f')
z=np.array([],dtype='f')
pitch=np.array([],dtype='f')
roll=np.array([],dtype='f')
yaw=np.array([],dtype='f')

tabx=np.array([],dtype='f')
taby=np.array([],dtype='f')
tabz=np.array([],dtype='f')
tabpitch=np.array([],dtype='f')
tabroll=np.array([],dtype='f')
tabyaw=np.array([],dtype='f')
def func_S(x, a, b, c, d, e, f, g):
 return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + (e * x**5) + (f * x**6)+g

def func_G(x, a, b, c, d):
 return np.exp(-0.5*((x-b)/c)**2)*a+d
def func_P(x, l, k):
    return l**k / math.factorial(k) * np.exp(-l)

def get_FWHM(c):
 return 2*c*(2*np.log(2))**0.5



for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-x"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-x", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.pickle', '')
        x=np.append(x, float(chan))
        tabx=np.append(tabx, float(g.flux))

sp = plt.subplot(321)
plt.plot(x, tabx, '.')

popt, pcov = curve_fit(func_G, x, tabx, p0=[max(tabx), sum(x*tabx)/sum(tabx), np.std(x), 0] )
x_line = np.arange(min(x), max(x), 1)
plt.plot(x_line, func_G(x_line, *popt), 'r-')
print('x_FWHM=%s'%get_FWHM( popt[2]))
for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-y"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-y", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.pickle', '')
        y=np.append(y, float(chan))
        taby=np.append(taby, g.flux)

sp = plt.subplot(322)
plt.plot(y, taby, '.')
popt, pcov = curve_fit(func_G, y, taby, p0=[max(taby), sum(y*taby)/sum(taby), np.std(y), 0] ) #среднеквадр
y_line = np.arange(min(y), max(y), 1)
plt.plot(y_line, func_G(y_line, *popt), 'r-')
print('y_FWHM=%s'%get_FWHM( popt[2]))

for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-z"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-z", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.pickle', '')
        z = np.append(z, float(chan))
        tabz=np.append(tabz, float(g.flux))

sp = plt.subplot(323)
plt.plot(z, tabz, '.')
popt, pcov = curve_fit(func_G, z, tabz, p0=[max(tabz), sum(z*tabz)/sum(tabz), np.std(z), 0])
z_line = np.arange(min(z), max(z), 1)
plt.plot(z_line, func_G(z_line, *popt), 'r-')
print('z_FWHM=%s'%get_FWHM( popt[2]))

for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-pitch"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-pitch", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.pickle', '')
        pitch = np.append(pitch, float(chan))
        tabpitch=np.append(tabpitch, g.flux)

sp = plt.subplot(324)
plt.plot(pitch, tabpitch, '.')
popt, pcov = curve_fit(func_G, pitch, tabpitch,p0=[max(tabpitch), sum(pitch*tabpitch)/sum(tabpitch), np.std(pitch), 0])
pitch_line = np.arange(min(pitch), max(pitch), 1)
plt.plot(pitch_line, func_G(pitch_line, *popt), 'r-')

for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-roll"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-roll", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.pickle', '')
        roll = np.append(roll, float(chan))
        tabroll=np.append(tabroll, g.flux)

sp = plt.subplot(325)
plt.plot(roll, tabroll, '.')
popt, pcov = curve_fit(func_G, roll, tabroll,p0=[max(tabroll), sum(roll*tabroll)/sum(tabroll), np.std(roll), 0])
roll_line = np.arange(min(roll), max(roll), 1)
plt.plot(roll_line, func_G(roll_line, *popt), 'r-')

for file in os.listdir(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-yaw"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(r"C:\Users\synchrotron\PycharmProjects\SKIF\change-yaw", file), 'rb'))
        temp, chan = file.split('_')
        chan=chan.replace('.pickle', '')
        yaw = np.append(yaw, float(chan))
        tabyaw=np.append(tabyaw, g.flux)

sp = plt.subplot(326)
plt.plot(yaw, tabyaw, '.')
popt, pcov = curve_fit(func_G, yaw, tabyaw, p0=[max(tabyaw), sum(yaw*tabyaw)/sum(tabyaw), np.std(yaw), 0])
yaw_line = np.arange(min(yaw), max(yaw), 1, )
plt.plot(yaw_line, func_G(yaw_line, *popt), 'r-')

plt.show()