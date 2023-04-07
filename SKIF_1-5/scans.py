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


from SKIF_1_5 import SKIF15

subdir = r"C:\Users\synchrotron\PycharmProjects\SKIF"

def change_x(plts, bl):
    scan_name = 'change-x'
    startX = bl.bentLaueCylinder01.center[0]
    for x in np.arange(-20., 20., 1):
        bl.bentLaueCylinder01.center[0] = startX+x
        for plot in plts:
            plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title +'_%s' % bl.bentLaueCylinder01.center[0] + '.png'
                                     )
            plot.persistentName = plot.saveName.replace('.png', '.pickle')
        yield

def change_y(plts, bl):
    scan_name = 'change-y'
    startY=bl.bentLaueCylinder01.center[1]
    for y in np.arange(-20., 20., 1):
        bl.bentLaueCylinder01.center[1] = startY+y
        for plot in plts:
            plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title +'_%s' % bl.bentLaueCylinder01.center[1] + '.png'
                                     )
            plot.persistentName = plot.saveName.replace('.png', '.pickle')
        yield

def change_z(plts, bl):
    scan_name = 'change-z'
    startZ=bl.bentLaueCylinder01.center[2]
    for z in np.arange(-20., 20., 1):
        bl.bentLaueCylinder01.center[2] = startZ+z
        for plot in plts:
            plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title +'_%s' % bl.bentLaueCylinder01.center[2] + '.png'
                                     )
            plot.persistentName = plot.saveName.replace('.png', '.pickle')
        yield

def change_pitch(plts, bl):
    scan_name = 'change-pitch'
    startP=bl.bentLaueCylinder01.pitch
    for pitch in np.arange(-30.e-6, 30.e-6, 1.e-6):
        bl.bentLaueCylinder01.pitch= startP+pitch
        for plot in plts:
            plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title +'_%s' % bl.bentLaueCylinder01.pitch + '.png'
                                     )
            plot.persistentName = plot.saveName.replace('.png', '.pickle')
        yield

def change_roll(plts, bl):
    scan_name = 'change-roll'
    startR=bl.bentLaueCylinder01.roll
    for roll in np.arange(-np.pi/180*3, np.pi/180*3, np.pi/180*0.5):
        bl.bentLaueCylinder01.roll = startR+roll
        for plot in plts:
            plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title +'_%s' % bl.bentLaueCylinder01.roll + '.png'
                                     )
            plot.persistentName = plot.saveName.replace('.png', '.pickle')
        yield
def change_yaw(plts, bl):
    scan_name = 'change-yaw'
    startYaw=bl.bentLaueCylinder01.yaw
    for yaw in np.arange(-np.pi/180*3, np.pi/180*3, np.pi/180*0.5):
        bl.bentLaueCylinder01.yaw = startYaw+yaw
        for plot in plts:
            plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title +'_%s' % bl.bentLaueCylinder01.yaw  + '.png'
                                     )
            plot.persistentName = plot.saveName.replace('.png', '.pickle')
        yield

def define_plots_x( bl):
    plots = []

    scan_name = 'change-x'
    if not os.path.exists(os.path.join(subdir, scan_name)):
        os.mkdir(os.path.join(subdir, scan_name))


    plots.append(xrtplot.XYCPlot(beam='screen01beamLocal01', title='plot-04,04,2023',
                                 xaxis=xrtplot.XYCAxis(label='z', unit='mm', data=raycing.get_z),
                                 yaxis=xrtplot.XYCAxis(label='x', unit='mm', data=raycing.get_x),
                                 aspect='auto', saveName='plot-03,04,2023.png'
                                  ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title + '-%sm' % bl.bentLaueCylinder01.center[0] + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots

def define_plots_y( bl):
    plots = []

    scan_name = 'change-y'
    if not os.path.exists(os.path.join(subdir, scan_name)):
        os.mkdir(os.path.join(subdir, scan_name))


    plots.append(xrtplot.XYCPlot(beam='screen01beamLocal01', title='plot-04,04,2023',
                                 xaxis=xrtplot.XYCAxis(label='z', unit='mm', data=raycing.get_z),
                                 yaxis=xrtplot.XYCAxis(label='x', unit='mm', data=raycing.get_x),
                                 aspect='auto', saveName='-%sm.png'%scan_name
                                  ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title + '-%sm' % bl.bentLaueCylinder01.center[1] + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots

def define_plots_z( bl):
    plots = []

    scan_name = 'change-z'
    if not os.path.exists(os.path.join(subdir, scan_name)):
        os.mkdir(os.path.join(subdir, scan_name))


    plots.append(xrtplot.XYCPlot(beam='screen01beamLocal01', title='plot-04,04,2023',
                                 xaxis=xrtplot.XYCAxis(label='z', unit='mm', data=raycing.get_z),
                                 yaxis=xrtplot.XYCAxis(label='x', unit='mm', data=raycing.get_x),
                                 aspect='auto', saveName='-%sm.png'%scan_name
                                  ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title + '-%sm' % bl.bentLaueCylinder01.center[2] + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots

def define_plots_pitch( bl):
    plots = []

    scan_name = 'change-pitch'
    if not os.path.exists(os.path.join(subdir, scan_name)):
        os.mkdir(os.path.join(subdir, scan_name))


    plots.append(xrtplot.XYCPlot(beam='screen01beamLocal01', title='plot-04,04,2023',
                                 xaxis=xrtplot.XYCAxis(label='z', unit='mm', data=raycing.get_z),
                                 yaxis=xrtplot.XYCAxis(label='x', unit='mm', data=raycing.get_x),
                                 aspect='auto', saveName='-%sm.png'%scan_name
                                  ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title + '-%sm' % bl.bentLaueCylinder01.pitch+ '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots

def define_plots_roll( bl):
    plots = []

    scan_name = 'change-roll'
    if not os.path.exists(os.path.join(subdir, scan_name)):
        os.mkdir(os.path.join(subdir, scan_name))


    plots.append(xrtplot.XYCPlot(beam='screen01beamLocal01', title='plot-04,04,2023',
                                 xaxis=xrtplot.XYCAxis(label='z', unit='mm', data=raycing.get_z),
                                 yaxis=xrtplot.XYCAxis(label='x', unit='mm', data=raycing.get_x),
                                 aspect='auto', saveName='-%sm.png'%scan_name
                                  ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title + '-%sm' % bl.bentLaueCylinder01.roll+ '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots

def define_plots_yaw( bl):
    plots = []

    scan_name = 'change-roll'
    if not os.path.exists(os.path.join(subdir, scan_name)):
        os.mkdir(os.path.join(subdir, scan_name))


    plots.append(xrtplot.XYCPlot(beam='screen01beamLocal01', title='plot-04,04,2023',
                                 xaxis=xrtplot.XYCAxis(label='z', unit='mm', data=raycing.get_z),
                                 yaxis=xrtplot.XYCAxis(label='x', unit='mm', data=raycing.get_x),
                                 aspect='auto', saveName='-%sm.png'%scan_name
                                  ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title + '-%sm' % bl.bentLaueCylinder01.yaw+ '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots

def main():
    beamLine = SKIF15()
    E0 = 30000

    beamLine.align_energy(E0, 100)
    beamLine.alignE = E0
    plots = define_plots_pitch(beamLine)
    scan=change_pitch
    xrtrun.run_ray_tracing(
        plots=plots,
        backend=r"raycing",
        repeats=2,
        beamLine=beamLine,
        generator=scan,
        generatorArgs=[plots, beamLine]
        )

    # beamLine.glow()

if __name__ == '__main__':
    main()
