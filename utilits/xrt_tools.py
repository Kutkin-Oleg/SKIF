import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
import os
import pickle

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

def crystal_focus(filename):
    data=pickle.load(open(filename, 'rb'))
    z = get_line_kb(data)
    k, b = z
    fdist = np.sign(k) * np.sqrt((1. / k) ** 2 + (b / k) ** 2)
    return (fdist)