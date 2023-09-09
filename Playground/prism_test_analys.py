from typing import List
from xrt.backends.raycing.sources import GeometricSource, Beam
from xrt.backends.raycing import BeamLine
from xrt.backends.raycing.materials import Material
from database.PrismaticLens import PrismaticLens
from xrt.backends.raycing.screens import Screen
from xrt.plotter import XYCAxis, XYCPlot
from xrt.backends.raycing import get_x, get_z, get_xprime, get_zprime
from utilits.xrtutils import get_integral_breadth, bell_fit
import xrt.backends.raycing.materials as rm

import xrt.backends.raycing.run as rrun
import xrt.runner as xrtrun

import numpy as np
import os
import shutil
import pickle

import matplotlib as mpl



Emap=np.linspace(20000, 100000, 10)
focus_formula=[]
data_dir = os.path.join( r"C:\Users\synchrotron\PycharmProjects\SKIF", 'datasets', 'tmp')
data_dir0 = os.path.join( r"C:\Users\synchrotron\PycharmProjects\SKIF", 'datasets', 'tmp')

crl_mat = Material('Be', rho=1.848, kind='lens')
crl_y_t = 1.2  # 0.6588  # mm
crl_y_g = 1.2  # 0.6588  # mm
crl_L = 270.  # 82.242  # mm

bl=CrocTestBL()
def slice_parabola(a, b, c, m):
    m += 1.
    x0 = -b / (2. * c)
    a_ = a + m * (b * b / (4 * c) - a)
    d = np.sqrt(b * b - 4 * a_ * c)
    x1 = (-b - d) / (2. * c)
    x2 = (-b + d) / (2. * c)
    return x0, x1, x2


for tempE in Emap:
    en=tempE
    focal_dist_calc = crl_y_g * crl_y_t / (crl_L * np.real(1. - crl_mat.get_refractive_index(en)))
    focus_formula.append(focal_dist_calc)
    for _ in range(4):
        pos, y_size = [], []
    for f_name in (os.path.join(data_dir, 'BeamFSSLocal_%.03f.pickle' % screen.center[1])
                   for screen in bl.FScreenStack):
        with open(f_name, 'rb') as f:
            y_size.append(get_integral_breadth(pickle.load(f), 'y'))
            pos.append(float(os.path.basename(f_name).replace('.pickle', '').replace('BeamFSSLocal_', '')))
    else:
        pos, y_size = np.array(pos), np.array(y_size)
        ii = np.argsort(pos)
        pos, y_size = pos[ii], y_size[ii]

        pp = np.polynomial.polynomial.Polynomial.fit(pos, y_size, 2)
        coef = pp.convert().coef
        focus, ymin, ymax = slice_parabola(*coef, 0.1)
        fig = mpl.pyplot.figure()
        ax = fig.add_subplot()
        ax.plot(pos, y_size)
        ax.plot(pos, pp(pos))
        ax.plot([focus, focus], [y_size.min(), y_size.max()], '--')
        ax.text(focus, y_size.max(), 'F=%.01f mm' % focus)
        fig.savefig(os.path.join(data_dir, '..', f'{en}eV_fdist%d.png' % _))

        focus_dict.append(focus / 4)


fig = mpl.pyplot.figure()
ax = fig.add_subplot()
ax.set_xlabel("Энергия, эВ")
ax.set_ylabel("Фокусное расстояние, мм")
ax.plot(Emap, focus_dict, 'x', label='xrt')
ax.plot(Emap, focus_formula, label='analitic')
ax.legend()
fig.savefig(os.path.join(data_dir, '..', 'focus(E).png'))