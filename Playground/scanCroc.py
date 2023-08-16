from typing import List
import os
import numpy as np
import matplotlib

matplotlib.use('agg')

import xrt.runner as xrtrun
import xrt.plotter as xrtplot
import xrt.backends.raycing as raycing

from utilits.xrtutils import get_minmax, get_line_kb, get_integral_breadth
import pickle
from Croccodile_Test import NSTU_SCW
from utilits.xrtutils import get_line_kb
subdir = r"C:\Users\synchrotron\PycharmProjects\SKIF\results"
E0="34000"

def change_screen(plts, beamline):
    scan_name = 'change-screen'
    if not os.path.exists(os.path.join(subdir, E0)):
        os.mkdir(os.path.join(subdir, E0))
    # for name in os.listdir(subdir):
    #     first, second = name.split('-',2)
    #     if first == 'find_diver':
    #         with open(name, 'rb') as f:
    #             data_new = pickle.load(f)
    #
    # temp = get_line_kb(data_new)
    # focus = (1 / temp[0] ** 2 + (temp[1] / temp[0] ** 2)) ** 0.5
    markStone=beamline.Screen.center[1]
    for exlen in np.linspace(-1000, 1000, 10):
        beamline.Screen.center[1] = markStone + exlen
        for plot in plts:
            plot.saveName = os.path.join(subdir, E0,
                                         plot.title + '_%s' % beamline.Screen.center[1] + '.png'
                                         )
            plot.persistentName = plot.saveName.replace('.png', '.mat')
        yield





def define_plots_find_diver( bl):
    plots = []

    scan_name = 'find_diver'
    if not os.path.exists(os.path.join(subdir, E0)):
        os.mkdir(os.path.join(subdir, E0))


    plots.append(xrtplot.XYCPlot(beam='ScreenLocal01', title='find_diver-16,08,2023',
                                 xaxis=xrtplot.XYCAxis(label=r'$z^{\prime}$', unit='', data=raycing.get_z),
                                 yaxis=xrtplot.XYCAxis(label=r'$x^{\prime}$', unit='', data=raycing.get_x),
                                 aspect='auto', saveName='-%sm.png'%scan_name
                                  ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, E0,
                                      plot.title + '-%sm' % bl.Screen.center[2] + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots

def define_plots_find_focus( bl):
    plots = []

    scan_name = 'find_focus'
    if not os.path.exists(os.path.join(subdir, E0)):
        os.mkdir(os.path.join(subdir, E0))


    plots.append(xrtplot.XYCPlot(beam='ScreenLocal01', title='Screen-16,08,2023',
                                 xaxis=xrtplot.XYCAxis(label='x', unit='mm', data=raycing.get_z),
                                 yaxis=xrtplot.XYCAxis(label='z', unit='mm', data=raycing.get_x),
                                 aspect='auto', saveName='-%sm.png'%scan_name
                                  ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, E0,
                                      plot.title + '-%sm' % bl.Screen.center[2] + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.mat')
    return plots




if __name__ == '__main__':
    check=False
    beamline = NSTU_SCW()
    repeats=1
    Energy=float(E0)
    beamline.align_energy( Energy,10,  mono=True)
    if  check:
        plots=define_plots_find_diver(beamline)
        scan=None
    else:
        scan = change_screen
        plots = define_plots_find_focus(beamline)

    xrtrun.run_ray_tracing(
                beamLine=beamline,
                plots=plots,
                repeats=repeats,
                backend=r"raycing",
                generator=scan,
                generatorArgs=[plots, beamline]
            )

    # beamline.glow()


