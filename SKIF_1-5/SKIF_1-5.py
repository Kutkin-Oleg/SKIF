# -*- coding: utf-8 -*-
"""

__author__ = "kutkin",
__date__ = "2023-04-03"




"""

import numpy as np
import sys
sys.path.append(r"C:\Users\synchrotron\AppData\Local\Programs\Python\Python310\lib\site-packages\xrt-1.4.0-py3.10.egg")
import xrt.backends.raycing.sources as rsources
import xrt.backends.raycing.screens as rscreens
import xrt.backends.raycing.materials as rmats
import xrt.backends.raycing.oes as roes
import xrt.backends.raycing.apertures as rapts
import xrt.backends.raycing.run as rrun
import xrt.backends.raycing as raycing
import xrt.plotter as xrtplot
import xrt.runner as xrtrun
import xrt.backends.raycing.myopencl as mcl
from "C:\Users\synchrotron\PycharmProjects\SKIF\database\CrystalSiPrecalc.py" import CrystalSiPrecalc
from BentLaueCylinder import BentLaueCylinder
import matplotlib.pyplot as plt
import xrt.backends.raycing.materials as rm
import pickle
import os

# crystalSi01 = rmats.CrystalSi(
#     hkl=(1, 1, 1),
#     t=2.,
#     geom=r"Laue reflected",
#     name=r"cr1",
#     useTT=True) #использовать уравнение  Takagi–Taupin

crystalSi01 = CrystalSiPrecalc(
    hkl=(1, 1, 1),
    t=2.,
    geom=r"Laue reflection",
    name=r"cr1",
    useTT=True)

# crystalSi02 = rmats.CrystalSi(
#     hkl=(1, 1, 1),
#     t=1.2,
#     geom=r"Laue reflected",
#     name=r"cr2",
#     useTT=True)

crystalSi02 = CrystalSiPrecalc(
    hkl=(1, 1, 1),
    t=2.,
    geom=r"Laue reflection",
    name=r"cr1",
    useTT=True)

def build_beamline():
    beamLine = raycing.BeamLine()

    beamLine.wiggler01 = rsources.Wiggler(
        bl=beamLine,
        nrays=100000,
        center=[0, 0, 0],
        eE=3,
        eI=0.4,
        eEspread=0.00135,
        eEpsilonX=0.09586,
        eEpsilonZ=0.009586,
        xPrimeMax=1.1,
        zPrimeMax=0.11,
        eMin=149900,#29900
        eMax=150100,#30100
        K=20.1685,
        period=48,
        n=18)

    beamLine.rectangularAperture01 = rapts.RectangularAperture(
        bl=beamLine,
        name=r"Front End Slit",
        center=[0, 15000, 0],
        opening=[-15, 15, -1.5, 1.5])

    beamLine.bentLaueCylinder01 = BentLaueCylinder(  # подставил свой класс вместо стандартного
        bl=beamLine,
        name=r"Si[111] Crystal 1",
        center=[0, 33500, 0],
        alpha=np.radians(35.3), #35.3
        pitch=2.252849714,#2.252849714,
        material=crystalSi01,
        limOptX=[-100.0, 100.0],
        limOptY=[-10.0, 10.0],
        targetOpenCL='CPU',
        R=np.inf)#np.inf

    beamLine.bentLaueCylinder01.ucl=mcl.XRT_CL(r'materials.cl', targetOpenCL='CPU')

    beamLine.screen02 = rscreens.Screen(
        bl=beamLine,
        name=r"Crystal 1-2 Monitor",
        center=[0, 33500, 12.5])

    beamLine.bentLaueCylinder02 = BentLaueCylinder(  # подставил свой класс вместо стандартного
        bl=beamLine,
        name=r"Si[111] Crystal 2",
        center=[0, 33688, 25],
        pitch=2.120945392,
        positionRoll=np.pi,
        material=crystalSi02,
        alpha=np.radians(35.3),
        limOptX=[-100.0, 100.0],
        limOptY=[-10.0, 10.0],
        targetOpenCL='CPU',
        R=np.inf)

    beamLine.screen01 = rscreens.Screen(
        bl=beamLine,
        name=r"Exit Monitor",
        center=[0, 114990, 25])

    beamLine.rectangularAperture02 = rapts.RectangularAperture(
        bl=beamLine,
        name=r"Exit Slits",
        center=[0, 111500, 25],
        opening=[-107.5, 107.5, -10, 10])

    def align_energy(self, en, d_en, mono=False):
        # changing energy for the beamline / source
        self.alignE = en
        if not mono:
            self.wiggler01.eMin = en * (1. - d_en)
            self.wiggler01.eMax = en * (1. + d_en)
        else:
            self.wiggler01.eMin = en - 1.
            self.wiggler01.eMax = en + 1.

        # Diffraction angle for the DCM
        theta0 = np.arcsin(rm.ch / (2 * self.bentLaueCylinder01.material.d * en))

        # Setting up DCM orientations / positions
        # Crystal 1
        self.bentLaueCylinder01.pitch = np.pi / 2 + theta0 + self.bentLaueCylinder01.alpha
        self.bentLaueCylinder01.center = [
            0.,
            33500,
            0.
        ]

        # Crystal 2
        self.bentLaueCylinder02.pitch = np.pi / 2 - theta0 + self.bentLaueCylinder02.alpha
        self.bentLaueCylinder02.center = [
            0.,
            33500. + 25/ np.tan(2. * theta0),
            25.
        ]

        # between-crystals monitor
        self.screen02.center = [
            0.,
            33500. + .5 * 25 / np.tan(2. * theta0),
            .5 * 25
        ]
    beamLine.align_energy=align_energy

    return beamLine


def run_process(beamLine):
    wiggler01beamGlobal01 = beamLine.wiggler01.shine()

    rectangularAperture01beamLocal01 = beamLine.rectangularAperture01.propagate(
        beam=wiggler01beamGlobal01)

    bentLaueCylinder01beamGlobal01, bentLaueCylinder01beamLocal01 = beamLine.bentLaueCylinder01.reflect(
        beam=wiggler01beamGlobal01)

    screen02beamLocal01 = beamLine.screen02.expose(
        beam=bentLaueCylinder01beamGlobal01)

    bentLaueCylinder02beamGlobal01, bentLaueCylinder02beamLocal01 = beamLine.bentLaueCylinder02.reflect(
        beam=bentLaueCylinder01beamGlobal01)

    screen01beamLocal01 = beamLine.screen01.expose(
        beam=bentLaueCylinder02beamGlobal01)

    rectangularAperture02beamLocal01 = beamLine.rectangularAperture02.propagate(
        beam=bentLaueCylinder02beamGlobal01)

    beamLine.prepare_flow()

    outDict = {
        'wiggler01beamGlobal01': wiggler01beamGlobal01,
        'rectangularAperture01beamLocal01': rectangularAperture01beamLocal01,
        'bentLaueCylinder01beamGlobal01': bentLaueCylinder01beamGlobal01,
        'bentLaueCylinder01beamLocal01': bentLaueCylinder01beamLocal01,
        'screen02beamLocal01': screen02beamLocal01,
        'bentLaueCylinder02beamGlobal01': bentLaueCylinder02beamGlobal01,
        'bentLaueCylinder02beamLocal01': bentLaueCylinder02beamLocal01,
        'screen01beamLocal01': screen01beamLocal01,
        'rectangularAperture02beamLocal01': rectangularAperture02beamLocal01}
    return outDict


rrun.run_process = run_process


def energy_allign(beam, en, de):
    theta_b = np.arcsin(rm.ch / (2. * en * crystalSi01.d))
    print(theta_b)
    beam.bentLaueCylinder01.pitch = np.pi / 2 + theta_b + beam.bentLaueCylinder02.alpha
    beam.bentLaueCylinder01.alpha = np.radians(35.3)
    theta_b = np.arcsin(rm.ch / (2. * en * crystalSi02.d))
    delz = 25 / np.tan(2 * theta_b)
    beam.bentLaueCylinder02.center = [0., 33500. + delz, 25.]
    beam.bentLaueCylinder02.pitch = np.pi / 2 - theta_b - beam.bentLaueCylinder02.alpha
    beam.bentLaueCylinder02.alpha = -np.radians(35.3)
    beam.screen02.center=[0., (33500.+33500.+delz)*0.5, 25.*0.5]
    beam.wiggler01.eMin=en-de/2
    beam.wiggler01.eMax = en + de / 2

    #theta_b=crystalSi01.get_dtheta_symmetric_Bragg(beam.alignE)



def get_minmax(data: xrtplot.SaveResults, axis: str ='x', fadeout: float=1e-3):
    if axis not in ('x', 'y', 'e'):
        raise ValueError()

    if axis == 'x':
        be = data.xbinEdges
        t1d = data.xtotal1D
    elif axis == 'y':
        be = data.ybinEdges
        t1d = data.ytotal1D
    elif axis == 'e':
        be = data.ebinEdges
        t1d = data.etotal1D
    else:
        return 0.
    t1d_xs = .5 * (be[1:] + be[:-1])
    t1d_dx = np.mean(be[1:] - be[:-1])
    t1d_xs = t1d_xs[t1d > fadeout * np.max(t1d)]

    return np.min(t1d_xs) - t1d_dx, np.max(t1d_xs) + t1d_dx

def test_plot(beam,E,L0):
    b=np.arcsin(rm.ch / (2. * E * crystalSi01.d))
    fi_0=np.radians(35.3)-b
    fi_h=np.radians(35.3)+b

    Rc=np.arange(-140., 140., 1.)
    # 1
    sp = plt.subplot(121)
    plt.plot(Rc, np.absolute(np.cos(fi_h))*np.cos(fi_h)*L0*Rc/(L0*(np.cos(fi_h)-np.cos(fi_0))+Rc*(np.cos(fi_0))**2))
    plt.title('расстояние до источника- {} м'.format(L0))
    plt.ylabel('Lh - расстояние до фокуса')
    plt.xlabel('Rc - радиус изгиба')
    plt.grid(True)
    plt.suptitle('Энергия {} эВ'.format(E))

    # 2
    sp = plt.subplot(122)
    L0=2*L0
    b = np.arcsin(rm.ch / (2. * E * crystalSi01.d))
    plt.plot(Rc, np.absolute(np.cos(fi_h))*np.cos(fi_h)*L0*Rc/(L0*(np.cos(fi_h)-np.cos(fi_0))+Rc*(np.cos(fi_0))**2))
    plt.title('расстояние до источника- {} м'.format(L0))
    plt.ylabel('Lh - расстояние до фокуса')
    plt.xlabel('Rc - радиус изгиба')
    plt.grid(True)


    plt.show()


def change_r(plts, bl):
    subdir = r"C:\Users\synchrotron\Desktop\science_days_GD\science_days"
    scan_name = 'get_focus_m'
    for r in np.arange(50000., 70000., 1000.):
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
    # yield здесь не нужен, он запустит второй раз последнее моделирование с r == np.inf

def define_plots( bl):
    plots = []
    subdir = r"C:\Users\synchrotron\Desktop\science_days_GD\science_days"
    scan_name = 'get_focus_m'
    if not os.path.exists(os.path.join(subdir, scan_name)):
        os.mkdir(os.path.join(subdir, scan_name))


    # plots.append(xrtplot.XYCPlot(beam='screen02beamLocal01', title='MD-XZ',
    #                              xaxis=xrtplot.XYCAxis('x'), yaxis=xrtplot.XYCAxis('z'),
    #                              aspect='auto', saveName='MD-XZ.png'))
    # plots[0].caxis.limits = [30000, 150000]
    # # plots[0].persistentName = 'test.pickle'
    #
    #
    # # главный косяк был в определении XYCAxis: он не понимал что ты хочешь вторую ось делать x' и рисовал всегда
    # # обе оси x, то есть всегда одинаковую прямую линию
    # plots.append(xrtplot.XYCPlot(beam='screen02beamLocal01', title='MD-XXpr',
    #                              xaxis=xrtplot.XYCAxis(label='x', unit='mm', data=raycing.get_x),
    #                              yaxis=xrtplot.XYCAxis(label=r'$x^{\prime}$', unit='', data=raycing.get_xprime),
    #                              aspect='auto', saveName='MD-XXpr.png'))
    # plots[1].persistentName = 'x-x.pickle'

    # то же самое с z'
    plots.append(xrtplot.XYCPlot(beam='screen02beamLocal01', title='MD-ZZpr',
                                 xaxis=xrtplot.XYCAxis(label='z', unit='mm', data=raycing.get_z),
                                 yaxis=xrtplot.XYCAxis(label=r'$z^{\prime}$', unit='', data=raycing.get_zprime),
                                 aspect='auto', saveName='MD-ZZpr.png'
                                  ))
    # plots[2].persistentName = 'z-z’.pickle'
    for plot in plots:
        plot.saveName = os.path.join(subdir, scan_name,
                                     plot.title + '-%sm' % bl.bentLaueCylinder01.R + '.png'
                                     )
        plot.persistentName = plot.saveName.replace('.png', '.pickle')
    return plots

def main():
    beamLine = build_beamline()
    E0 = 30000 # ниже 30 лучше не ставить, там не все данные есть
    energy_allign(beamLine, E0, 2000) # полосу энергии пошире поставил на всякий случай, можно назад вернуть
    beamLine.alignE=E0
    plots = define_plots(beamLine)
    scan=change_r
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
