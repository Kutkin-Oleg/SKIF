import os
import numpy as np
import matplotlib
matplotlib.use('agg')
import xrt.runner as xrtrun
import xrt.plotter as xrtplot
import xrt.backends.raycing as raycing

from SKIF_NSTU_SCW import SKIFNSTU
from utilits.xrt_tools import crystal_focus

resol='mat'
E0 = 30000
subdir=rf"C:\Users\synchrotron\PycharmProjects\SKIF\SKIF_NSTU_SCW\results\{resol}\{E0}\R-R"


def define_plots(bl):
    plots = []
    scan_name = 'change-screen-%s'  % (bl.bentLaueCylinder02.Rx)
    if not os.path.exists(os.path.join(subdir, scan_name)):
        os.mkdir(os.path.join(subdir, scan_name))


    plots.append(xrtplot.XYCPlot(beam='screen03beamLocal01', title='Sample-XZ',
                                 xaxis=xrtplot.XYCAxis(label='x', unit='mm', data=raycing.get_x),
                                 yaxis=xrtplot.XYCAxis(label='z', unit='mm', data=raycing.get_z),
                                 aspect='auto', saveName='Sample-XZ.png'
                                  ))
    for plot in plots:
        plot.saveName = os.path.join(subdir, scan_name,
                                     plot.title + '-%sm' % bl.bentLaueCylinder02.Rx + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', f'.{resol}')
    return plots

def define_plots_diver(bl):
    plots = []
    scan_name = 'diver-screen-'
    if not os.path.exists(os.path.join(subdir, scan_name)):
        os.mkdir(os.path.join(subdir, scan_name))
    plots.append(xrtplot.XYCPlot(beam='screen02beamLocal01', title=f'{scan_name}',
                                 xaxis=xrtplot.XYCAxis(label='x', unit='mm', data=raycing.get_x),
                                 yaxis=xrtplot.XYCAxis(label=r'$x^{\prime}$', unit='', data=raycing.get_xprime),
                                 aspect='auto', saveName=f'{scan_name}_Sample-XX.png'
                                 ))
    for plot in plots:
        plot.saveName = os.path.join(subdir,scan_name,
                                     plot.title + '-%sm' % bl.bentLaueCylinder01.Rx + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', f'.pickle')
    return plots

def change_screen(plts, bl):
    scan_name = 'change-screen-%s' % (bl.bentLaueCylinder02.Rx)
    d0=bl.screen03.center[1]
    for dist in np.linspace(-500., 500., 50):

        bl.screen03.center[1]=d0+dist
        for plot in plts:
            plot.xaxis.limits=None
            plot.yaxis.limits = None
            plot.caxis.limits = None
            plot.saveName = os.path.join(subdir, scan_name,
                                     plot.title + '_%s' % bl.screen03.center[1] + '.png'
                                     )
            plot.persistentName = plot.saveName.replace('png', f'{resol}')
        yield

def main():
    beamLine = SKIFNSTU()
    diver=False

    dist0=beamLine.bentLaueCylinder02 .center[1]
    beamLine.align_energy(E0, 1000)
    beamLine.alignE = E0


    # for R in np.linspace(-2000., -500., 5):
    #     beamLine.bentLaueCylinder01.Rx = R
    #     beamLine.bentLaueCylinder02.Rx = R
    #     beamLine.bentLaueCylinder01.Ry = R/1.e6
    #     beamLine.bentLaueCylinder02.Ry = R/1.e6
    #     plots = define_plots(beamLine)
    #     scan = change_screen
    #     if (diver==False):
    #         beamLine.screen03.center[1] = dist0+crystal_focus(subdir +
    #                                                 '\diver-screen-\diver-screen-' + '-%sm' % beamLine.bentLaueCylinder01.Rx + '.pickle')
    #     if diver:
    #         scan = None
    #         plots = define_plots_diver(beamLine)
    #
    #
    #     xrtrun.run_ray_tracing(
    #         plots=plots,
    #         backend=r"raycing",
    #         repeats=5,
    #         beamLine=beamLine,
    #         generator=scan,
    #         generatorArgs=[plots, beamLine]
    #         )
    #     beamLine.screen03.center[1]=dist0+10000
    beamLine.glow()

if __name__ == '__main__':
    main()