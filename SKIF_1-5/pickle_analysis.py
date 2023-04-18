import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
import os

def get_line_kb(data, show=False):
    """
    :param data: assuming that y axis is z', x axis is z, c axis is energy
    :return:
    """

    xvals = .5 * (data.xbinEdges[1:] + data.xbinEdges[
                                       :-1])  # создание графика на основе данных границ столбцов гистограмм
    yvals = .5 * (data.ybinEdges[1:] + data.ybinEdges[:-1])
    xvals_, yvals_ = np.meshgrid(xvals, yvals)

    def f(kb):
        return np.sum(data.total2D * (yvals_ - xvals_ * np.tan(kb[0]) - kb[1]) ** 2)

    min_res = minimize(f, np.array([.1, .1]), bounds=[(-np.pi / 2, np.pi / 2), (-1., 1.)])

    if show:
        plt.imshow(data.total2D, aspect='auto', origin='lower',
                   extent=[data.xbinEdges.min(), data.xbinEdges.max(),
                           data.ybinEdges.min(), data.ybinEdges.max()])
        plt.plot(xvals, xvals * np.tan(min_res.x[0]) + min_res.x[1])

        plt.xlim(data.xbinEdges.min(), data.xbinEdges.max())
        plt.ylim(data.ybinEdges.min(), data.ybinEdges.max())
        plt.show()

    return np.tan(min_res.x[0]), min_res.x[1]








tab=[]
Rc=[]
E=30000
for file in os.listdir(fr"C:\Users\synchrotron\PycharmProjects\SKIF\change-r-30000.0"):
    if file.endswith(".pickle"):
        g=pickle.load(open(os.path.join(fr"C:\Users\synchrotron\PycharmProjects\SKIF\change-r-30000.0", file), 'rb'))
        el, chan = file.split('_')
        chan=chan.replace('.0.pickle', '' )
        Rc.append(int(chan)/1000)
        z=get_line_kb(g)
        # tab.append((1-z[1]/z[0])/z[0])
        k, b = z
        fdist = -np.sign(k) * np.sqrt((1. / k) ** 2 + (b / k) ** 2)
        tab.append(fdist/1000)

L0=33.5
# Rc = np.arange(-100., 100., 10.)
# Rc=[ -100, -90, -80, -70, -60, -50, -40, -30, -20, 10, 20, 30, 40, 50, 60, 70, 80, 90,100,110,120,130,140]
b = np.arcsin(12398. / (2. * E * 3.157))

fi_0 = np.radians(35.3) + b
fi_h = np.radians(35.3) - b
plt.plot(Rc, tab, '.')
Rd = np.arange(-150., 150, 0.2)
plt.plot(Rd, -np.absolute(np.cos(fi_h))*L0*Rd/(2*L0-np.cos(fi_0)*Rd))
# plt.plot(Rd, -np.cos(fi_h)**2*np.cos(fi_h)*L0*Rd/((np.absolute(np.cos(fi_h))+np.cos(fi_0))*L0-np.cos(fi_0)**2*Rd))
plt.title('расстояние до источника- {} м'.format(L0))
plt.ylim([-500, 500])
plt.xlim([-50, 150])
plt.ylabel('Lh - расстояние до фокуса, м')
plt.xlabel('Rc - радиус изгиба, м')
plt.grid(True)
plt.suptitle(f'Энергия {E} эВ')
plt.grid(True)
plt.savefig(f'pickle_e={E}.png')
plt.show()