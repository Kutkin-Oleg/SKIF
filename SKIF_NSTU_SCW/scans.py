import os
import numpy as np
import matplotlib
matplotlib.use('agg')
import xrt.runner as xrtrun
import xrt.plotter as xrtplot
import xrt.backends.raycing as raycing

from SKIF_NSTU_SCW import SKIFNSTU

subdir=r"C:\Users\synchrotron\PycharmProjects\SKIF\SKIF_NSTU_SCW\results"
def define_plots(bl):
    plots = []
    scan_name = 'change-screen-%s'  % (bl.bentLaueCylinder01.R)
    if not os.path.exists(os.path.join(subdir, scan_name)):
        os.mkdir(os.path.join(subdir, scan_name))


    plots.append(xrtplot.XYCPlot(beam='screen03beamLocal01', title='Sample-XZ',
                                 xaxis=xrtplot.XYCAxis(label='x', unit='mm', data=raycing.get_x),
                                 yaxis=xrtplot.XYCAxis(label='z', unit='mm', data=raycing.get_z),
                                 aspect='auto', saveName='Sample-XZ.png'
                                  ))
    for plot in plots:
        plot.saveName = os.path.join(subdir, scan_name,
                                     plot.title + '-%sm' % bl.bentLaueCylinder01.R + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots

def change_screen(plts, bl):
    scan_name = 'change-screen-%s' % (bl.bentLaueCylinder01.R)
    d0=bl.screen03.center[1]
    for dist in np.arange(0., 150000., 10000.):
        bl.screen03.center[1]=d0+dist
        for plot in plts:
            plot.saveName = os.path.join(subdir, scan_name,
                                     plot.title + '_%s' % bl.screen03.center[1] + '.png'
                                     )
            plot.persistentName = plot.saveName.replace('.png', '.mat')
        yield

def main():
    beamLine = SKIFNSTU()



    E0 = 60000
    # beamLine.bentLaueCylinder01.R = -5000
    dist0=beamLine.screen03.center[1]
    beamLine.align_energy(E0, 10)
    beamLine.alignE = E0
    for R in np.arange(-140000., 140000., 10000.):
        beamLine.bentLaueCylinder01.R = R
        beamLine.bentLaueCylinder02.R = -R
        plots = define_plots(beamLine)
        scan = change_screen
        xrtrun.run_ray_tracing(
            plots=plots,
            backend=r"raycing",
            repeats=5,
            beamLine=beamLine,
            generator=scan,
            generatorArgs=[plots, beamLine]
            )
        beamLine.screen03.center[1]=dist0

    beamLine.glow()

if __name__ == '__main__':
    main()