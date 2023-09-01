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
E0="50000"
Center=120000

def change_screen(plts, beamline):
    scan_name = 'change-screen'
    if not os.path.exists(os.path.join(subdir, E0)):
        os.mkdir(os.path.join(subdir, E0))
    # for name in os.listdir(os.path.join(subdir, E0)):
    #     first, second = name.split('-')
    #     if (first == 'find_diver') and name.endswith(".pickle"):
    #         data_new = pickle.load(open(os.path.join(subdir,E0, name), 'rb'))
    #
    # temp = get_line_kb(data_new)
    # focus = (1 / temp[0] ** 2 + (temp[1] / temp[0] ** 2)) ** 0.5
    # print(focus)
    markStone=beamline.Screen.center[1]
    for exlen in np.linspace(-20000, 20000, 20):
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

    # source = xrtplot.XYCPlot(
    #     beam=r"BeamSourceGlobal",
    #     xaxis=xrtplot.XYCAxis(
    #         label=r"x",
    #         unit=r"um",
    #         fwhmFormatStr=r"%.3f"),
    #     yaxis=xrtplot.XYCAxis(
    #         label=r"z",
    #         unit=r"um",
    #         fwhmFormatStr=r"%.3f"),
    #     caxis=xrtplot.XYCAxis(
    #         label=r"energy",
    #         unit=r"eV"),
    #     aspect=r"auto",
    #     title=r"source",
    #     fluxKind=r"power",
    #     saveName='Source.png')
    # plots.append(source)


    plots.append(xrtplot.XYCPlot(beam='ScreenLocal01', title='find_diver-16,08,2023',
                                 xaxis=xrtplot.XYCAxis(label=r'z', unit='mm', data=raycing.get_z,fwhmFormatStr=r"%.3f"),
                                 yaxis=xrtplot.XYCAxis(label=r'$z^{\prime}$', unit='', data=raycing.get_zprime,fwhmFormatStr=r"%.3f", limits=[0,2.e-6]),
                                 aspect='auto', saveName='-%sm.png'%scan_name
                                  ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, E0,
                                      plot.title + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots



def define_plots_find_focus( bl):
    plots = []

    scan_name = 'find_focus'
    if not os.path.exists(os.path.join(subdir, E0)):
        os.mkdir(os.path.join(subdir, E0))

    # source = xrtplot.XYCPlot(
    #     beam=r"BeamSourceGlobal",
    #     xaxis=xrtplot.XYCAxis(
    #         label=r"x",
    #         unit=r"um",
    #         fwhmFormatStr=r"%.3f"),
    #     yaxis=xrtplot.XYCAxis(
    #         label=r"z",
    #         unit=r"um",
    #         fwhmFormatStr=r"%.3f"),
    #     caxis=xrtplot.XYCAxis(
    #         label=r"energy",
    #         unit=r"eV"),
    #     aspect=r"auto",
    #     title=r"source",
    #     fluxKind=r"p",
    #     saveName='Source.png')
    # plots.append(source)

    plots.append(xrtplot.XYCPlot(beam='ScreenLocal01', title='Screen-18,08,23',
                                 xaxis=xrtplot.XYCAxis(label='z', unit='um', data=raycing.get_z,fwhmFormatStr=r"%.3f"),
                                 yaxis=xrtplot.XYCAxis(label='x', unit='um', data=raycing.get_x,fwhmFormatStr=r"%.3f"),
                                 aspect='auto', saveName='-%sm.png'%scan_name
                                  ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, E0,
                                      plot.title + '-%sm' % bl.Screen.center[2] + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.mat')
    return plots


def define_plots_cool_grath( bl):
    plots = []
    bl.Screen_free.center[1]=Center
    scan_name = 'cool_grath'
    if not os.path.exists(os.path.join(subdir, E0, scan_name)):
        if not os.path.exists(os.path.join(subdir, E0)):
            os.mkdir(os.path.join(subdir,E0, scan_name))
        else:
            os.mkdir(os.path.join(subdir , E0, scan_name))

    source = xrtplot.XYCPlot(
        beam=r"BeamSourceGlobal",
        xaxis=xrtplot.XYCAxis(
            label=r"x",
            unit=r"um",
            data=raycing.get_x,
            fwhmFormatStr=r"%.3f"),
        yaxis=xrtplot.XYCAxis(
            label=r"z",
            unit=r"um",
            data=raycing.get_z,
            fwhmFormatStr=r"%.3f"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV"),
        aspect=r"auto",
        title=r"source",
        saveName='Source.png', fluxKind='total')
    plots.append(source)


    plots.append(xrtplot.XYCPlot(beam='ScreenLocal01', title='screen-23,08,2023',
                                 xaxis=xrtplot.XYCAxis(label=r'z', unit='um', data=raycing.get_z,fwhmFormatStr=r"%.3f"),
                                 yaxis=xrtplot.XYCAxis(label=r'x', unit='um', data=raycing.get_x,fwhmFormatStr=r"%.3f"),
                                 aspect='auto', saveName='screen.png', fluxKind='total'
                                  ))
    plots.append(xrtplot.XYCPlot(beam='Screen_freeLocal01', title='screen_free-23,08,2023',
                                 xaxis=xrtplot.XYCAxis(label=r'z', unit='um', data=raycing.get_z,
                                                       fwhmFormatStr=r"%.3f"),
                                 yaxis=xrtplot.XYCAxis(label=r'x', unit='um', data=raycing.get_x,
                                                       fwhmFormatStr=r"%.3f"),
                                 aspect='auto', saveName='screen_free.png',fluxKind='total'
                                 ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, E0,scan_name,
                                      plot.title + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.mat')
    return plots

def define_plots_cool_grath_div( bl):
    plots = []
    bl.Screen_free.center[1]=40000
    scan_name = 'cool_grath'
    if not os.path.exists(os.path.join(subdir, E0, scan_name)):
        os.mkdir(os.path.join(subdir, E0, scan_name))

    source = xrtplot.XYCPlot(
        beam=r"BeamSourceGlobal",
        xaxis=xrtplot.XYCAxis(
            label=r"$x^{\prime}$",
            data=raycing.get_xprime,
            unit=r"",
            fwhmFormatStr=r"%.3f"),
        yaxis=xrtplot.XYCAxis(
            label=r"$z^{\prime}$",
            data=raycing.get_zprime,
            unit=r"",
            fwhmFormatStr=r"%.3f"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV"),
        aspect=r"auto",
        title=r"source_div",
        saveName='Source_div.png', fluxKind='total')
    plots.append(source)


    plots.append(xrtplot.XYCPlot(beam='ScreenLocal01', title='screen_div-23,08,2023',
                                 xaxis=xrtplot.XYCAxis(label=r"$x^{\prime}$", unit='urad', data=raycing.get_xprime,fwhmFormatStr=r"%.3f"),
                                 yaxis=xrtplot.XYCAxis(label=r"$z^{\prime}$", unit='rad', data=raycing.get_zprime,fwhmFormatStr=r"%.3f"),
                                 aspect='auto', saveName='screen_div.png', fluxKind='total'
                                  ))
    plots.append(xrtplot.XYCPlot(beam='Screen_freeLocal01', title='screen_free_div-23,08,2023',
                                 xaxis=xrtplot.XYCAxis(label=r"$x^{\prime}$", unit='rad', data=raycing.get_xprime,
                                                       fwhmFormatStr=r"%.3f"),
                                 yaxis=xrtplot.XYCAxis(label=r"$z^{\prime}$", unit='rad', data=raycing.get_zprime,
                                                       fwhmFormatStr=r"%.3f"),
                                 aspect='auto', saveName='screen_free_div.png',fluxKind='total'
                                 ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, E0,scan_name,
                                      plot.title + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.mat')
    return plots

if __name__ == '__main__':
    check=False
    beamline = NSTU_SCW()
    repeats=1
    Energy=float(E0)
    beamline.align_energy( Energy,0.01)
    beamline.Screen.center[1]=Center
    # if  check:
    #     plots=define_plots_find_diver(beamline)
    #     scan=None
    # else:
    #     scan = change_screen
    #     plots = define_plots_find_focus(beamline)
    #
    # xrtrun.run_ray_tracing(
    #     beamLine=beamline,
    #     plots=plots,
    #     repeats=repeats,
    #     backend=r"raycing",
    #     generator=scan,
    #     generatorArgs=[plots, beamline]
    # )


    xrtrun.run_ray_tracing(
                beamLine=beamline,
                plots=define_plots_cool_grath_div(beamline),
                repeats=repeats,
                backend=r"raycing",
                generator=None,
                generatorArgs=[define_plots_cool_grath_div(beamline), beamline]
            )

    # beamline.glow()


