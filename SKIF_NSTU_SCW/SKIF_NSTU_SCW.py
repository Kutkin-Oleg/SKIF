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
from database.CrystalSiPrecalc import CrystalSiPrecalc
from database.BentLaueParaboloidWithBump import BentLaueParaboloidWithBump
import matplotlib.pyplot as plt
import xrt.backends.raycing.materials as rm
import pickle
import os
from params.source import ring_kwargs, wiggler_nstu_scw_kwargs
from params.params_NSTU_SCW import front_end_distance, front_end_opening, front_end_v_angle, front_end_h_angle, \
    monochromator_distance, monochromator_z_offset, monochromator_x_lim, monochromator_y_lim


crystalSi01 = CrystalSiPrecalc(database='/Users/synchrotron/PycharmProjects/SKIF/database/Si111ref_sag.csv',
    hkl=(1, 1, 1),
    t=0.5,
    geom=r"Laue reflection",
    name=r"cr1",
    useTT=True)


crystalSi02 = CrystalSiPrecalc(database='/Users/synchrotron/PycharmProjects/SKIF/database/Si111ref_sag.csv',
    hkl=(1, 1, 1),
    t=0.5,
    geom=r"Laue reflection",
    name=r"cr2",
    useTT=True)

class SKIFNSTU(raycing.BeamLine):
    def __init__(self):

        raycing.BeamLine.__init__(self)
        self.name = r"SKIF_1_5"

        self.wiggler01 = rsources.Wiggler(
            name=r"wiggler01",
            bl=self,
            nrays=100000,
            center=[0, 0, 0],
            eMin=29900,
            eMax=30100,
            xPrimeMax=front_end_h_angle * .505e3,
            zPrimeMax=front_end_v_angle * .505e3,
            **ring_kwargs,
            **wiggler_nstu_scw_kwargs,

        )

        self.rectangularAperture01 = rapts.RectangularAperture(
            bl=self,
            name=r"Front End Slit",
            center=[0, front_end_distance, 0],
            opening=front_end_opening)

        self.bentLaueCylinder01 = BentLaueParaboloidWithBump(
            bl=self,
            name=r"Si[111] Crystal 1",
            center=[0, 33500, 0],
            alpha=np.radians(35.3),  # 35.3
            pitch=np.pi/2,  # 2.252849714,
            roll=0.,
            yaw=0.,
            material=crystalSi01,
            limPhysY=monochromator_y_lim,
            limOptY=monochromator_y_lim,
            limPhysX=monochromator_x_lim,
            limOptX=monochromator_x_lim,
            targetOpenCL='CPU',
            Rx=-2000,
            Ry=2000*1.e6)

        self.bentLaueCylinder01.ucl = mcl.XRT_CL(r'materials.cl', targetOpenCL='CPU')

        self.bentLaueCylinder02 = BentLaueParaboloidWithBump(
            bl=self,
            name=r"Si[111] Crystal 1",
            center=[0, 33500, 25],
            alpha=np.radians(-35.3),  # 35.3
            pitch=np.pi / 2,  # 2.252849714,
            roll=0.,
            yaw=0.,
            material=crystalSi01,
            limPhysY=monochromator_y_lim,
            limOptY=monochromator_y_lim,
            limPhysX=monochromator_x_lim,
            limOptX=monochromator_x_lim,
            targetOpenCL='CPU',
            Rx=-2000,
            Ry=2000 * 1.e6)
        self.screen02 = rscreens.Screen(
            bl=self,
            name=r"Crystal 1-2 Monitor",
            center=[0, monochromator_distance, monochromator_z_offset/2])



        self.screen01 = rscreens.Screen(
            bl=self,
            name=r"Apper Monitor",
            center=[0, 35500 - 10,  monochromator_z_offset])

        self.rectangularAperture02 = rapts.RectangularAperture(
            bl=self,
            name=r"Exit Slits",
            center=[0, 35500, 25],
            opening=[-107.5*100, 107.5*100, -10*100, 10*100])

        self.screen03 = rscreens.Screen(
            bl=self,
            name=r"Exit Monitor",
            center=[0, 36000, monochromator_z_offset])



    def align_energy(self, en, de):
        theta_b = np.arcsin(rm.ch / (2. * en * crystalSi01.d))
        print(theta_b)
        self.bentLaueCylinder01.alpha = np.radians(35.3)
        self.bentLaueCylinder01.pitch = np.pi / 2 + theta_b + self.bentLaueCylinder02.alpha
        theta_b = np.arcsin(rm.ch / (2. * en * crystalSi02.d))
        delz = 25 / np.tan(2 * theta_b)
        self.bentLaueCylinder02.center = [0., 33500. + delz, 25.]
        self.bentLaueCylinder02.alpha = np.radians(-35.3)
        self.bentLaueCylinder02.pitch = np.pi / 2 - theta_b + self.bentLaueCylinder02.alpha
        self.screen02.center = [0., (33500. + 33500. + delz) * 0.5, 25. * 0.5]
        self.wiggler01.eMin = en - de / 2
        self.wiggler01.eMax = en + de / 2





def run_process(beamLine: SKIFNSTU):
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

    screen03beamLocal01 = beamLine.screen03.expose(
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
        'rectangularAperture02beamLocal01': rectangularAperture02beamLocal01,
        'screen03beamLocal01': screen03beamLocal01}
    return outDict


rrun.run_process = run_process


