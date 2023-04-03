from typing import List
import os
import numpy as np
import pandas as pd
import pickle
import matplotlib
matplotlib.use('agg')

import xrt.runner as xrtrun
import xrt.plotter as xrtplot
import xrt.backends.raycing as raycing


from SKIF_1_5 import SKIF15, energy_allign

subdir = r"C:\Users\synchrotron\PycharmProjects\SKIF"

def change_x(plts, bl):
    scan_name = 'change_x'
    for x in np.arange(-40., 40., 1.):
        bl.bentLaueCylinder01.center[1] = x
        for plot in plts:
            plot.saveName = os.path.join(subdir, scan_name,
                                     plot.title + '_%s' % bl.bentLaueCylinder01.center[1] + '.png'
                                     )
            if x<0:
                plot.saveName = os.path.join(subdir, scan_name,
                                             plot.title + '!_%s' % bl.bentLaueCylinder01.center[1] + '.png'
                                             )
            plot.persistentName = plot.saveName.replace('.png', '.pickle')
        yield


def define_plots( bl):
    plots = []

    scan_name = 'change_x'
    if not os.path.exists(os.path.join(subdir, scan_name)):
        os.mkdir(os.path.join(subdir, scan_name))


    plots.append(xrtplot.XYCPlot(beam='screen02beamLocal01', title='plot_03,04,2023',
                                 xaxis=xrtplot.XYCAxis(label='z', unit='mm', data=raycing.get_z),
                                 yaxis=xrtplot.XYCAxis(label='x', unit='', data=raycing.get_zprime),
                                 aspect='auto', saveName='plot_03,04,2023.png'
                                  ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, scan_name,
                                     plot.title + '-%sm' % bl.bentLaueCylinder01.R + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots

def main():
    beamLine = SKIF15()
    E0 = 150000
    # energy_allign(beamLine, E0, 2000)
    beamLine.align_energy(E0, 2000)
    plots = define_plots(beamLine)
    scan=change_x
    xrtrun.run_ray_tracing(
        plots=plots,
        backend=r"raycing",
        repeats=2,
        beamLine=beamLine,
        generator=scan,
        generatorArgs=[plots, beamLine]
        )


    beamLine.glow()
    # test_plot(beamLine, E0, 33.5)

if __name__ == '__main__':
    main()
