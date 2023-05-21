import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import curve_fit




def func_S(x, a, b, c, d, e):
 return (a * x) + (b * x**2) + (c * x**3) + d

def func_L(x, a, x0, y,  d):
 return a/(1+((x-x0)/y)**2)+d

def func_G(x, a, b, c, d):
 return np.exp(-0.5*((x-b)/c)**2)*a+d

def get_G_FWHM(c):
 return 2*c*(2*np.log(2))**0.5

def get_FWHM(x, y):
    maxy=0.5*max(y)
    # print('FW = %s' % maxy)

    mid=(abs(max(x))+min(x))/2

    FWHM=0.
    for i in np.arange(round(len(x)/2), len(x), 1):
        if (y[i] >= maxy*0.99) and (y[i] <= maxy*1.01):
            FWHM=abs(x[i]-mid)
            # print('max1 = %s' % y[i])
            break

    for i in np.arange(round(len(x)/2), 0, -1):
        if (y[i] >= maxy * 0.99) and (y[i] <= maxy * 1.01):
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

def get_plot(x, tabx, name, step, sp):

    popt, pcov = curve_fit(func_G, x, tabx, p0=[max(tabx), sum(x * tabx) / sum(tabx), np.std(x), 0])
    x_line = np.arange(min(x), max(x), step)
    poptL, pcovL = curve_fit(func_L, x, tabx, p0=[max(tabx), sum(x * tabx) / sum(tabx), step/1.e-2, 0])
    poptS, pcovS = curve_fit(func_S, x, tabx, p0=[1,1, 1,1,0])
    line = np.arange(min(x), max(x), step/100)
    hmfL = half_max_x(line*2, func_L(line, *poptL))
    print(f'{name}_Lor_ FWHM ={(poptL[2] * 2)}')
    print(f'{name}_Lor_(FWHM)={get_FWHM(line, func_L(line, *poptL))}')
    print(f'{name}_Gau_ FWHM ={get_G_FWHM(popt[2])}')
    print(f'{name}_Gau_(FWHM)={get_FWHM(line, func_G(line, *popt))}')
    print(f'{name}_Lag_(FWHM)={get_FWHM(line, lagrange(x, tabx, line))} \n')
    print(f'{name}_Lor_WEB_(FWHM)={hmfL[1] - hmfL[0]}\n')
    plt.ylim([0, 1.e13])
    sp.set_title(f'{name}')
    plt.plot(x, tabx, 'b.', label = 'ray tracing')
    plt.plot(line, lagrange(x, tabx, line), 'g-', label = 'Lagrange')
    plt.plot(x_line, func_G(x_line, *popt), 'r-', label = 'Gaussian')
    plt.plot(x_line, func_L(x_line, *poptL), 'y-', label = 'Lorentz')
    plt.legend()

    return plt.plot

def lin_interp(x, y, i, half):
    return x[i] + (x[i+1] - x[i]) * ((half - y[i]) / (y[i+1] - y[i]))

def half_max_x(x, y):
    half = max(y)/2.0
    signs = np.sign(np.add(y, -half))
    zero_crossings = (signs[0:-2] != signs[1:-1])
    zero_crossings_i = np.where(zero_crossings)[0]
    return [lin_interp(x, y, zero_crossings_i[0], half),
            lin_interp(x, y, zero_crossings_i[1], half)]


x=np.array([],dtype='f')
tabx=np.array([],dtype='f')

data=['x', 'y', 'z', 'pitch', 'roll', 'yaw']
borders=[1, 1, 1, 1.e-6, 1.e-3, 1.e-3]
positions=[321, 322, 323, 324, 325, 326]
for i in np.arange(0, len(data), 1):
    for file in os.listdir(fr"C:\Users\synchrotron\PycharmProjects\SKIF\change-{data[i]}"):
        if file.endswith(".pickle"):
            g = pickle.load(open(os.path.join(rf"C:\Users\synchrotron\PycharmProjects\SKIF\change-{data[i]}", file), 'rb'))
            temp, chan = file.split('_')
            chan = chan.replace('.pickle', '')
            x = np.append(x, float(chan))
            tabx = np.append(tabx, float(g.flux))

    sp = plt.subplot(positions[i])
    get_plot(x, tabx, f'{data[i]}', borders[i], sp)
    x=[]
    tabx=[]

print('(FWHM) - функция определяющая пшпв написанная мной, FWHM считается по формулам для распределений')
plt.show()