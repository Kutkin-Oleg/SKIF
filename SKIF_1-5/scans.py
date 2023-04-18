import os
import numpy as np
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
    for x in np.arange(-200., 200., 10):
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
    for y in np.arange(100., 160., 5):
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
    for pitch in np.arange(-20.e-6, 20.e-6, 1.e-6):
        bl.bentLaueCylinder01.extraPitch=pitch
        for plot in plts:
            plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title +'_%s' % bl.bentLaueCylinder01.extraPitch + '.png'
                                     )
            plot.persistentName = plot.saveName.replace('.png', '.pickle')
        yield

def change_roll(plts, bl):
    scan_name = 'change-roll'
    for roll in np.arange(-20.e-3, 20.e-3, 1.e-3):
        bl.bentLaueCylinder01.extraRoll = roll
        for plot in plts:
            plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title +'_%s' % bl.bentLaueCylinder01.extraRoll + '.png'
                                     )
            plot.persistentName = plot.saveName.replace('.png', '.pickle')
        yield
def change_yaw(plts, bl):
    scan_name = 'change-yaw'
    for yaw in np.arange(-40.e-3, 50.e-3, 5.e-3):
        bl.bentLaueCylinder01.extraYaw = yaw
        for plot in plts:
            plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title +'_%s' % bl.bentLaueCylinder01.extraYaw  + '.png'
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
                                      plot.title + '-%sm' % bl.bentLaueCylinder01.extraPitch+ '.png'
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
                                      plot.title + '-%sm' % bl.bentLaueCylinder01.extraRoll+ '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots

def define_plots_yaw( bl):
    plots = []

    scan_name = 'change-yaw'
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
                                      plot.title + '-%sm' % bl.bentLaueCylinder01.extraYaw+ '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots
def find_focus(plts, bl):
    scan_name = 'focus-%s'%bl.bentLaueCylinder01.R
    for y in np.arange(100., 350., 10.):
        bl.screen01.center[1] = y*1000+bl.bentLaueCylinder01.center[1]
        bl.rectangularAperture02.center[1] = bl.screen01.center[1]+100

        for plot in plts:
            plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title +'_%s' % y + '.png'
                                     )
            plot.persistentName = plot.saveName.replace('.png', '.pickle')
        yield
def define_plots_y_focus( bl):
    plots = []

    scan_name = 'focus-%s'%bl.bentLaueCylinder01.R
    if not os.path.exists(os.path.join(subdir, scan_name)):
        os.mkdir(os.path.join(subdir, scan_name))


    plots.append(xrtplot.XYCPlot(beam='screen01beamLocal01', title='plot-04,04,2023',
                                 xaxis=xrtplot.XYCAxis(label='x', unit='mm', data=raycing.get_x),
                                 yaxis=xrtplot.XYCAxis(label='z', unit='mm', data=raycing.get_z),
                                 aspect='auto', saveName='plot-03,04,2023.png'
                                  ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, scan_name,
                                      plot.title + '-%sm' % bl.screen01.center[1] + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots

def change_r(plts, bl):
    scan_name = 'change-r-%s'  % ((bl.wiggler01.eMax+bl.wiggler01.eMin)/2)
    for r in np.arange(70000., 140000., 1000.):
        bl.bentLaueCylinder01.R = r
        for plot in plts:
            plot.saveName = os.path.join(subdir, scan_name,
                                     plot.title + '_%s' % bl.bentLaueCylinder01.R + '.png'
                                     )
            if r<0:
                plot.saveName = os.path.join(subdir, scan_name,
                                             plot.title + '!_%s' % bl.bentLaueCylinder01.R + '.png'
                                             )
            plot.persistentName = plot.saveName.replace('.png', '.pickle')
        yield


def define_plots_change_r(bl):
    plots = []
    scan_name = 'change-r-%s' % ((bl.wiggler01.eMax+bl.wiggler01.eMin)/2)
    if not os.path.exists(os.path.join(subdir, scan_name)):
        os.mkdir(os.path.join(subdir, scan_name))


    plots.append(xrtplot.XYCPlot(beam='screen02beamLocal01', title='MD-ZZpr',
                                 xaxis=xrtplot.XYCAxis(label='z', unit='mm', data=raycing.get_z),
                                 yaxis=xrtplot.XYCAxis(label=r'$z^{\prime}$', unit='', data=raycing.get_zprime),
                                 aspect='auto', saveName='MD-ZZpr.png'
                                  ))
    for plot in plots:
        plot.saveName = os.path.join(subdir, scan_name,
                                     plot.title + '-%sm' % bl.bentLaueCylinder01.R + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots

def main():
    beamLine = SKIF15()
    E0 = 30000
    # beamLine.bentLaueCylinder01.R = -125000
    beamLine.align_energy(E0, 1)
    beamLine.alignE = E0
    plots = define_plots_change_r(beamLine)
    scan=change_r
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
