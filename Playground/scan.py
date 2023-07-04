import os
import numpy as np
import matplotlib
matplotlib.use('agg')
import xrt.runner as xrtrun
import xrt.plotter as xrtplot
import xrt.backends.raycing as raycing
import scipy.io
from SKIF_NSTU_LENSES import SKIFNSTU
import xraydb
from utilits.xrt_tools import crystal_focus
resol='mat'
E0 = 30000
subdir=rf"C:\Users\synchrotron\PycharmProjects\SKIF\Playground\results\{E0}\R-R"

def change_lenses_par(filename, bl):
    # data = scipy.io.loadmat(filename)
    # div=float(data['dy'])
    # length=(bl.doubleParaboloidLens02.limPhysX[1]*2)*div
    # f=crystal_focus(subdir +'\diver-screen-\diver-screen-' + '-%sm' % bl.bentLaueCylinder01.Rx + '.pickle')
    bl.doubleParaboloidLens02.center[1]=31000
    print(f'положение лииз {bl.doubleParaboloidLens02.center[1]}')
    material = 'Be'
    # density gr/sm^3
    density = 1.848
    # Focus length of lenses m
    focus=5000
    # radius of curvation m
    R = 0.5e-3
    temp = xraydb.xray_delta_beta(material, density, E0)
    N = round(R / (2 * temp[0] * focus))
    N=500
    print(f'количество линз  {N}')
    # bl.doubleParaboloidLens02.nCRL=N
    return ()


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
    plots.append(xrtplot.XYCPlot(beam='screen01beamLocal01', title=f'{scan_name}',
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




def main():
    beamLine = SKIFNSTU()
    diver=False

    dist0=beamLine.bentLaueCylinder02 .center[1]
    beamLine.align_energy(E0, 100)
    beamLine.alignE = E0
    beamLine.bentLaueCylinder01.Rx = -500
    beamLine.bentLaueCylinder02.Rx = -500
    beamLine.bentLaueCylinder01.Ry = 500*6
    beamLine.bentLaueCylinder02.Ry = 500*6



    for R in np.linspace(-630., -630., 1):
        beamLine.bentLaueCylinder01.Rx = R
        beamLine.bentLaueCylinder02.Rx = R
        beamLine.bentLaueCylinder01.Ry = -R*6
        beamLine.bentLaueCylinder02.Ry = -R*6
        plots = define_plots(beamLine)
        scan = None
        if (diver==False):

            change_lenses_par(subdir +'\diver-screen-\diver-screen-' + '-%sm' % beamLine.bentLaueCylinder01.Rx + '.mat', beamLine)
        if diver:
            scan = None
            beamLine.screen01.center[1] = 90000
            beamLine.doubleParaboloidLens02.center[1] = 90000
            plots = define_plots_diver(beamLine)


        # xrtrun.run_ray_tracing(
        #     plots=plots,
        #     backend=r"raycing",
        #     repeats=5,
        #     beamLine=beamLine,
        #     generator=scan,
        #     generatorArgs=[plots, beamLine]
        #     )
        beamLine.glow()
        beamLine.screen03.center[1]=dist0+10000
    # beamLine.glow()

if __name__ == '__main__':
    main()