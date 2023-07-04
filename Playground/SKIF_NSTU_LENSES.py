# -*- coding: utf-8 -*-
"""

__author__ = "kutkin",
__date__ = "2023-06-19"




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
from database.BentLaueParaboloidWithBump import BentLaueParaboloid
import matplotlib.pyplot as plt
import xrt.backends.raycing.materials as rm
import pickle
import os
from params.source import ring_kwargs, wiggler_nstu_scw_kwargs
from params.params_NSTU_SCW import   monochromator_z_offset, monochromator_x_lim, monochromator_y_lim

front_end_distance = 2500  # from source
front_end_h_angle = 2.0e-3  # rad
front_end_v_angle = 0.2e-3  # rad
front_end_opening = [
    -front_end_distance * np.tan(front_end_h_angle / 2.),
    front_end_distance * np.tan(front_end_h_angle / 2.),
    -front_end_distance * np.tan(front_end_v_angle / 2.),
    front_end_distance * np.tan(front_end_v_angle / 2.)
]


monochromator_distance=5000
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

Be = rmats.Material(
    elements=r"Be",
    kind=r"lens",
    rho=1.85,
    name=None)

class SKIFNSTU(raycing.BeamLine):
    def __init__(self):

        raycing.BeamLine.__init__(self)
        self.name = r"SKIF_1_5"

        self.OE_for_source = rapts.RectangularAperture(
            bl=self,
            name=r"OE_for_source",
            center=[0, 1500, 0],
            opening=[-1.5, 1.5, -0.15, 0.15])


        self.source=rsources.GaussianBeam(
            bl=self,
            name='source',
            center=(0, 0, 0),
            w0=[4.133e-11/(np.pi*2e-3)*1000, 4.133e-11/(np.pi*0.2e-3)],
            distE='flat',
            energies=(29990, 30010),
            energyWeights=None,
            polarization='h',
            pitch=0,
            yaw=0)

        self.rectangularAperture01 = rapts.RectangularAperture(
            bl=self,
            name=r"Front End Slit",
            center=[0, front_end_distance, 0],
            opening=front_end_opening)

        self.bentLaueCylinder01 = BentLaueParaboloid(
            bl=self,
            name=r'Si[111] Crystal 1',
            center=[0., monochromator_distance, 0.],
            pitch=np.pi / 2.,
            roll=0.,
            yaw=0.,
            alpha=np.radians(35.3),
            material=(crystalSi01,),
            r_for_refl='x',
            targetOpenCL='CPU',
            limPhysY=monochromator_y_lim,
            limOptY=monochromator_y_lim,
            limPhysX=monochromator_x_lim,
            limOptX=monochromator_x_lim,
            Rx=-1000,
            Ry=1000 * 1.e6)


        self.screen02 = rscreens.Screen(
            bl=self,
            name=r"Crystal 1-2 Monitor",
            center=[0, 15000, monochromator_z_offset/2])

        self.bentLaueCylinder02 = BentLaueParaboloid(
            bl=self,
            name=r'Si[111] Crystal 2',
            center=[0., monochromator_distance, monochromator_z_offset],
            positionRoll=np.pi,
            pitch=0.,
            roll=0.,
            yaw=0.,
            alpha=np.radians(35.3),
            material=(crystalSi02,),
            r_for_refl='x',
            targetOpenCL='CPU',
            limPhysY=monochromator_y_lim,
            limOptY=monochromator_y_lim,
            limPhysX=monochromator_x_lim,
            limOptX=monochromator_x_lim,
            Rx=-1000,
            Ry=1000*1.e6)

        self.screen01 = rscreens.Screen(
            bl=self,
            name=r"Apper Monitor",
            center=[0, 15500 - 10,  monochromator_z_offset])

        self.rectangularAperture02 = rapts.RectangularAperture(
            bl=self,
            name=r"Exit Slits",
            center=[0, 18000, monochromator_z_offset],
            opening=[-107.5*100, 107.5*100, -10*100, 10*100])

        self.doubleParaboloidLens02 = roes.DoubleParaboloidLens(
            bl=self,
            name=r'doubleParaboloidLens02',
            center=[0, 20000, monochromator_z_offset],
            pitch=1.5707963267948966,
            material=Be,
            limPhysX=[-1.39/2, 1.39/2],
            limPhysY=[-1.39/2, 1.39/2],
            shape=r"round",
            t=0.03,
            focus=0.25,
            zmax=0.5,
            nCRL=160,
            targetOpenCL='CPU',)

        self.screen03 = rscreens.Screen(
            bl=self,
            name=r"Exit Monitor",
            center=[0, 60000, monochromator_z_offset])



    def align_energy(self, en, de):
        theta0 = np.arcsin(rm.ch / (2 * self.bentLaueCylinder01.material[0].d * en))
        self.bentLaueCylinder01.pitch = np.pi / 2 + theta0 + self.bentLaueCylinder01.alpha
        self.bentLaueCylinder01.center = [0., monochromator_distance, 0.]
        delz = monochromator_z_offset / np.tan(2. * theta0)
        self.bentLaueCylinder02.center = [0., monochromator_distance + delz, 25.]
        self.bentLaueCylinder02.pitch = np.pi / 2 - theta0 + self.bentLaueCylinder02.alpha
        self.screen02.center = [0., monochromator_distance + delz * 0.5, 25. * 0.5]
        self.source.energies = (en-de/2,en+de/2)





def run_process(beamLine: SKIFNSTU):


    waveOnFSMg=beamLine.OE_for_source.prepare_wave(
        prevOE=beamLine.source,
        nrays=100000,
        rw=None)

    sourcebeamGlobal01 = beamLine.source.shine(wave=waveOnFSMg)

    rectangularAperture01beamLocal01 = beamLine.rectangularAperture01.propagate(
        beam=sourcebeamGlobal01)

    bentLaueCylinder01beamGlobal01, bentLaueCylinder01beamLocal01 = beamLine.bentLaueCylinder01.reflect(
        beam=sourcebeamGlobal01)

    screen02beamLocal01 = beamLine.screen02.expose(
        beam=bentLaueCylinder01beamGlobal01)

    bentLaueCylinder02beamGlobal01, bentLaueCylinder02beamLocal01 = beamLine.bentLaueCylinder02.reflect(
        beam=bentLaueCylinder01beamGlobal01)

    screen01beamLocal01 = beamLine.screen01.expose(
        beam=bentLaueCylinder02beamGlobal01)

    rectangularAperture02beamLocal01 = beamLine.rectangularAperture02.propagate(
        beam=bentLaueCylinder02beamGlobal01)
    doubleParaboloidLens02beamGlobal01, doubleParaboloidLens02beamLocal101, doubleParaboloidLens02beamLocal201 =beamLine.doubleParaboloidLens02.multiple_refract(
        beam=bentLaueCylinder02beamGlobal01)

    screen03beamLocal01 = beamLine.screen03.expose(
        beam=doubleParaboloidLens02beamGlobal01)

    beamLine.prepare_flow()

    outDict = {

        'source01beamGlobal01': sourcebeamGlobal01,
        'rectangularAperture01beamLocal01': rectangularAperture01beamLocal01,
        'bentLaueCylinder01beamGlobal01': bentLaueCylinder01beamGlobal01,
        'bentLaueCylinder01beamLocal01': bentLaueCylinder01beamLocal01,
        'screen02beamLocal01': screen02beamLocal01,
        'bentLaueCylinder02beamGlobal01': bentLaueCylinder02beamGlobal01,
        'bentLaueCylinder02beamLocal01': bentLaueCylinder02beamLocal01,
        'screen01beamLocal01': screen01beamLocal01,
        'rectangularAperture02beamLocal01': rectangularAperture02beamLocal01,
        'doubleParaboloidLens02beamGlobal01': doubleParaboloidLens02beamGlobal01,
        'doubleParaboloidLens02beamLocal101': doubleParaboloidLens02beamLocal101,
        'doubleParaboloidLens02beamLocal201': doubleParaboloidLens02beamLocal201,
        'screen03beamLocal01': screen03beamLocal01}
    return outDict


rrun.run_process = run_process


