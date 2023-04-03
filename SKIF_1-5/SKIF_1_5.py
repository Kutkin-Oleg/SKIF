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
from database.BentLaueCylinder import BentLaueCylinder
import matplotlib.pyplot as plt
import xrt.backends.raycing.materials as rm
import pickle
import os
from params.source import ring_kwargs, wiggler_1_5_kwargs
from params.params_1_5 import front_end_distance, front_end_opening, front_end_v_angle, front_end_h_angle, \
    monochromator_distance, monochromator_z_offset, monochromator_x_lim, monochromator_y_lim, \
    exit_slit_distance, exit_slit_opening, filter1_distance, filter2_distance, filter3_distance, filter4_distance, \
    filter5_distance, diamond_filter_thickness, sic_filter_thickness, focusing_distance


crystalSi01 = CrystalSiPrecalc(
    hkl=(1, 1, 1),
    t=2.,
    geom=r"Laue reflection",
    name=r"cr1",
    useTT=True)


crystalSi02 = CrystalSiPrecalc(
    hkl=(1, 1, 1),
    t=2.,
    geom=r"Laue reflection",
    name=r"cr2",
    useTT=True)

class SKIF15(raycing.BeamLine):
    def __init__(self):
        raycing.BeamLine.__init__(self)
        self.name = r"SKIF_1_5"

        self.wiggler01 = rsources.Wiggler(
            bl=self,
            nrays=100000,
            center=[0, 0, 0],
            eMin=100000,
            eMax=170000,
            xPrimeMax=front_end_h_angle * .505e3,
            zPrimeMax=front_end_v_angle * .505e3,
            **ring_kwargs,
            **wiggler_1_5_kwargs
        )

        self.rectangularAperture01 = rapts.RectangularAperture(
            bl=self,
            name=r"Front End Slit",
            center=[0, front_end_distance, 0],
            opening=front_end_opening)

        self.bentLaueCylinder01 = BentLaueCylinder(
            bl=self,
            name=r"Si[111] Crystal 1",
            center=[0, monochromator_distance, monochromator_z_offset],
            alpha=np.radians(35.3),
            pitch=2.252849714,
            material=crystalSi01,
            limOptX=monochromator_x_lim ,
            limOptY=monochromator_y_lim,
            targetOpenCL='CPU',
            R=np.inf)

        self.screen02 = rscreens.Screen(
            bl=self,
            name=r"Crystal 1-2 Monitor",
            center=[0, 33500, 12.5])

        self.bentLaueCylinder02 = BentLaueCylinder(
            bl=self,
            name=r"Si[111] Crystal 2",
            center=[0, 33688, 25],
            pitch=2.120945392,
            positionRoll=np.pi,
            material=crystalSi02,
            alpha=np.radians(35.3),
            limOptX=monochromator_x_lim,
            limOptY=monochromator_y_lim,
            targetOpenCL='CPU',
            R=np.inf)

        self.screen01 = rscreens.Screen(
            bl=self,
            name=r"Crystal 1-2 Monitor",
            center=[0, monochromator_distance, .5 * monochromator_z_offset])

        self.rectangularAperture02 = rapts.RectangularAperture(
            bl=self,
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





def run_process(beamLine: SKIF15):
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

rrun.run_process = run_process


