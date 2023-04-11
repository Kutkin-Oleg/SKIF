import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import curve_fit


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
def func_S(x, a, b, c, d, e, f, g, h, i):
 return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + (e * x**5) + (f * x**6)+(g* x**7)+(h** x**6)+i

def func_G(x, a, b, c, d):
 return np.exp(-0.5*((x-b)/c)**2)*a+d


def get_G_FWHM(c):
 return 2*c*(2*np.log(2))**0.5

def get_FWHM(x, y, maxy):
    maxy=0.5*maxy
    # print('FW = %s' % maxy)
    if min(x)<0:
        mid=(abs(max(x))-abs(min(x)))/2
    else:
        mid=(abs(max(x))+abs(min(x)))/2

    FWHM=0.
    for i in np.arange(round(len(x)/2), len(x), 1):
        if (y[i] >= maxy*0.98) and (y[i] <= maxy*1.02):
            FWHM=abs(x[i]-mid)
            # print('max1 = %s' % y[i])
            break

    for i in np.arange(round(len(x)/2), 0, -1):
        if (y[i] >= maxy * 0.98) and (y[i] <= maxy * 1.02):
            FWHM=(FWHM+abs(x[i]-mid))
            # print('max2 = %s' % y[i])
            break
    return FWHM

def lagrange(x, y, t):
    """
    Find the Lagrange polynomial through the points (x, y) and return its value at t.
    """
    # Lagrange Interpolation Method  [By Bottom Science]

    # Check that the input arrays have the same length
    if len(x) != len(y):
        raise ValueError("The arrays x and y must have the same length.")
    p = 0
    for i in range(len(x)):
        xi, yi = x[i], y[i]
        term = yi
        for j in range(len(x)):
            if i == j:
                continue
            term *= (t - x[j]) / (xi - x[j])
        p += term
    return p

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
y_line =[]
line =np.arange(min(x), max(x), 0.5)
for i in np.arange(0, len(line), 1):
    y_line =np.append(y_line, lagrange(x, tabx, line[i]))
plt.ylim([0, 1.e13])
plt.plot(line, y_line, 'g-')
print('x_G_FWHM=%s' % get_G_FWHM(popt[2]))
print('x_FWHM=%s' % get_FWHM(line, y_line, max(tabx)))

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
print('y_G_FWHM=%s' % get_G_FWHM(popt[2]))

y_line =[]
line =np.arange(min(y), max(y), 0.5)
for i in np.arange(0, len(line), 1):
    y_line =np.append(y_line, lagrange(y, taby, line[i]))
plt.ylim([0, 1.e13])
plt.plot(line, y_line, 'g-')
print('y_FWHM=%s' % get_FWHM(line, y_line, max(taby)))

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
print('z_G_FWHM=%s' % get_G_FWHM(popt[2]))

y_line=[]
line =np.arange(min(z), max(z), 0.1)
for i in np.arange(0, len(line), 1):
    y_line =np.append(y_line, lagrange(z, tabz, line[i]))
plt.ylim([0, 1.e13])
plt.plot(line, y_line, 'g-')
print('Z_FWHM=%s' % get_FWHM(line, y_line, max(tabz)))

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
pitch_line = np.arange(min(pitch), max(pitch), 1.e-6)
plt.plot(pitch_line, func_G(pitch_line, *popt), 'r-')
print('pitch_G_FWHM=%s' % get_G_FWHM(popt[2]))

y_line=[]
line =np.arange(min(pitch), max(pitch), 1.e-6)
for i in np.arange(0, len(line), 1):
    y_line =np.append(y_line, lagrange(pitch, tabpitch, line[i]))
plt.ylim([0, 1.e13])
plt.plot(line, y_line, 'g-')
print('pitch_FWHM=%s' % get_FWHM(line, y_line, max(tabpitch)))

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
roll_line = np.arange(min(roll), max(roll), 1.e-3)
plt.plot(roll_line, func_G(roll_line, *popt), 'r-')
print('roll_G_FWHM=%s' % get_G_FWHM(popt[2]))

y_line=[]
line =np.arange(min(roll), max(roll), 0.1e-3)
for i in np.arange(0, len(line), 1):
    y_line =np.append(y_line, lagrange(roll, tabroll, line[i]))
plt.ylim([0, 1.e13])
plt.plot(line, y_line, 'g-')
print('roll_FWHM=%s' % get_FWHM(line, y_line, max(tabroll)))


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
yaw_line = np.arange(min(yaw), max(yaw), 1.e-3, )
plt.plot(yaw_line, func_G(yaw_line, *popt), 'r-')
print('yaw_G_FWHM=%s' % get_G_FWHM(popt[2]))

y_line=[]
line =np.arange(min(yaw), max(yaw), 1.e-3)
for i in np.arange(0, len(line), 1):
    y_line =np.append(y_line, lagrange(yaw, tabyaw, line[i]))
plt.ylim([0, 1.e13])
plt.plot(line, y_line, 'g-')
print('yaw_FWHM=%s' % get_FWHM(line, y_line, max(tabyaw)))

plt.show()