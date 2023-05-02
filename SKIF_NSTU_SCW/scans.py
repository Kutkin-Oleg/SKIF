import os
import numpy as np
import matplotlib
matplotlib.use('agg')
import xrt.runner as xrtrun
import xrt.plotter as xrtplot
import xrt.backends.raycing as raycing

from SKIF_NSTU_SCW import SKIFNSTU

def main():
    beamLine = SKIFNSTU()
    E0 = 60000
    # beamLine.bentLaueCylinder01.R = -125000
    beamLine.align_energy(E0, 1000)
    beamLine.alignE = E0
    # plots = define_plots_get_f(beamLine, 110, 100)
    # scan=change_r
    # generator=scan,
    # xrtrun.run_ray_tracing(
    #     plots=plots,
    #     backend=r"raycing",
    #     repeats=2,
    #     beamLine=beamLine,
    #
    #     generatorArgs=[plots, beamLine]
    #     )

    beamLine.glow()

if __name__ == '__main__':
    main()