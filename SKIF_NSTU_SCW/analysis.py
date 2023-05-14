import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
import os
import scipy.io

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



def find_scales(data, show=True):
    xvals = .5 * (data.xbinEdges[1:] + data.xbinEdges[:-1])  # создание графика на основе данных границ столбцов гистограмм
    yvals = .5 * (data.ybinEdges[1:] + data.ybinEdges[:-1])
    xvals_, yvals_ = np.meshgrid(xvals, yvals)


    if show:
        plt.imshow(data.total2D, aspect='auto', origin='lower',
                   extent=[data.xbinEdges.min(), data.xbinEdges.max(),
                           data.ybinEdges.min(), data.ybinEdges.max()])


        plt.xlim(data.xbinEdges.min(), data.xbinEdges.max())
        plt.ylim(data.ybinEdges.min(), data.ybinEdges.max())

        plt.show()

    return





for file in os.listdir(fr"C:\\Users\synchrotron\PycharmProjects\SKIF\SKIF_NSTU_SCW\results\change-screen--140000.0"):
    if file.endswith(".mat"):
        g=scipy.io.loadmat(open(os.path.join(fr"C:\Users\synchrotron\PycharmProjects\SKIF\SKIF_NSTU_SCW\results\change-screen--140000.0", file), 'rb'))
        # find_scales(g)
        print(file)




# print(file)
# plt.title('расстояние до источника- {} м')
# plt.ylim([-500, 500])
# plt.xlim([-50, 150])
#
# plt.grid(True)
#
# plt.show()