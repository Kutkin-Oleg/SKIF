from typing import List
import os
import numpy as np
import matplotlib

matplotlib.use('agg')

import xrt.runner as xrtrun
import xrt.plotter as xrtplot
import xrt.backends.raycing as raycing

from utilits.xrtutils import get_minmax, get_line_kb, get_integral_breadth

from Croccodile_Test import NSTU_SCW


E0=30.e3

if __name__ == '__main__':
    beamline = NSTU_SCW()
    beamline.align_energy(E0, 10)
    beamline.glow()


