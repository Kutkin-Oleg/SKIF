import numpy as np
from copy import deepcopy
import os

import xrt.backends.raycing.sources as rsources
import xrt.backends.raycing.screens as rscreens
import xrt.backends.raycing.apertures as rapts
import xrt.backends.raycing.materials as rm
import xrt.backends.raycing.run as rrun
import xrt.backends.raycing as raycing
import xrt.backends.raycing.oes as roe

from database import CrystalSiPrecalc, BentLaueParaboloid, CrocLens
from database.CrystalSiPrecalc import CrystalSiPrecalc
from database.BentLaueParaboloid import BentLaueParaboloid
from database.CrocLens import CrocLens
from params.source import ring_kwargs, wiggler_nstu_scw_kwargs, wiggler_1_5_kwargs
from params.params_NSTU_SCW import front_end_distance, front_end_opening, front_end_v_angle, front_end_h_angle, \
    monochromator_x_lim, monochromator_y_lim, \
    exit_slit_distance, crl_mask_distance

BASE_DIR = 'C:/Users/synchrotron/PycharmProjects/SKIF'
# ################################################# SETUP PARAMETERS ###################################################

"""CrocLens"""
croc_crl_distance=27000
croc_crl_L=270
croc_crl_y_t=1.2
alignment_energy = 30.e3


# #################################################### MATERIALS #######################################################



mBeryllium = rm.Material('Be', rho=1.848, kind='lens')
mAl = rm.Material('Al', rho=2.7, kind='lens')
mDiamond = rm.Material('C', rho=3.5, kind='lens')
mGraphite = rm.Material('C', rho=2.15, kind='lens')
lens_material = mBeryllium


# #################################################### BEAMLINE ########################################################


class NSTU_SCW(raycing.BeamLine):
    def __init__(self):
        raycing.BeamLine.__init__(self)

        self.name = "NSTU SCW"
        self.alignE = alignment_energy

        self.SuperCWiggler = rsources.GeometricSource(
            bl=self,
            name='',
            center=(0, 0, 0),
            nrays=10000,
            distx='normal',
            dx=0.455/2.355,
            disty=None,
            dy=0,
            distz='normal',
            dz=0.027/2.355,
            distxprime='flat',
            dxprime=[0, 2.e-6],
            distzprime='flat',
            dzprime=[0, 0.2e-6],
            distE='flat',
            energies=(alignment_energy-1, alignment_energy+1),
            energyWeights=None,
            polarization='horizontal',
            filamentBeam=False,
            uniformRayDensity=False,
            pitch=0,
            yaw=0
        )





        self.FrontEnd = rapts.RectangularAperture(
            bl=self,
            name=r"Front End Slit",
            center=[0, front_end_distance, 0],
            opening=front_end_opening
        )



        self.CrlMask = rapts.RectangularAperture(
            bl=self,
            name=r"Front End Slit",
            center=[0, crl_mask_distance, 0],
            opening=front_end_opening
        )

        self.CrocLensStack = CrocLens.make_stack(
            L=croc_crl_L, N=int(croc_crl_L), d=croc_crl_y_t, g_left=0., g_right=croc_crl_y_t,
            bl=self,
            center=[0., croc_crl_distance, 0],
            material=lens_material,
            limPhysX=monochromator_x_lim,
            limPhysY=monochromator_y_lim,
        )

        self.Screen = rscreens.Screen(
            bl=self,
            name=r"Screen",
            center=[0, 42000, 0],
        )

    def print_positions(self):
        print('#' * 20, self.name, '#' * 20)

        for element in (self.SuperCWiggler, self.FrontEnd,
                         self.Screen):
            print('#' * 5, element.name, 'at', element.center)



        print('#' * (42 + len(self.name)))



    def align_energy(self, en, d_en, mono=False, invert_croc=False):
        # changing energy for the beamline / source
        self.alignE = en
        if not mono:
            self.SuperCWiggler.energies = (en * (1 - d_en), en * (1 + d_en))
        else:
            self.SuperCWiggler.energies = (en - 1, en + 1)

        # re-making the CRL
        del self.CrocLensStack[:]
        if invert_croc:
            g_l, g_r = CrocLens.calc_y_g(lens_material, croc_crl_distance / 2., en, croc_crl_y_t, croc_crl_L), 0
        else:
            g_l, g_r = 0, CrocLens.calc_y_g(lens_material, croc_crl_distance / 2., en, croc_crl_y_t, croc_crl_L)

        self.CrocLensStack = CrocLens.make_stack(
            L=croc_crl_L, N=int(croc_crl_L), d=croc_crl_y_t, g_left=g_l, g_right=g_r,
            bl=self,
            center=[0., croc_crl_distance, 0],
            material=lens_material,
            limPhysX=monochromator_x_lim,
            limPhysY=monochromator_y_lim,
        )

        # setting up pre-CRL mask
        apt = CrocLens.calc_optimal_params(lens_material, croc_crl_distance / 2., en)['Aperture']
        self.CrlMask.opening = [-100., 100., -apt / 2., apt / 2.]
        print('Croc Lens: g_r = %.01f, g_l = %.01f, y_t = %.01f, L = %.01f' % (g_r, g_l, croc_crl_y_t, croc_crl_L))
        print('Mask: %.01f' % apt)
        self.print_positions()
# ################################################# BEAM TOPOLOGY ######################################################


def run_process(bl: NSTU_SCW):
    beam_source = bl.SuperCWiggler.shine()

    beam_ap1 = bl.FrontEnd.propagate(
        beam=beam_source
    )

    outDict = {
        'BeamSourceGlobal': beam_source,
        'BeamAperture1Local': beam_ap1,
    }
    beamIn = beam_source

    # Pre-CRL mask
    outDict['BeamAperture2Local'] = bl.CrlMask.propagate(
        beam=beamIn
    )

    # CRL
    for ilens, lens in enumerate(bl.CrocLensStack):
        lglobal, llocal1, llocal2 = lens.double_refract(beamIn, needLocal=True)
        strl = '_{0:02d}'.format(ilens)
        outDict['BeamLensGlobal' + strl] = lglobal
        outDict['BeamLensLocal1' + strl] = llocal1
        outDict['BeamLensLocal2' + strl] = llocal2

        llocal2a = raycing.sources.Beam(copyFrom=llocal2)
        llocal2a.absorb_intensity(beamIn)
        outDict['BeamLensLocal2a' + strl] = llocal2a
        beamIn = lglobal

    ScreenLocal01 = bl.Screen.expose(
        beam=beamIn
    )
    outDict['ScreenLocal01']= ScreenLocal01

    bl.prepare_flow()

    return outDict


rrun.run_process = run_process

