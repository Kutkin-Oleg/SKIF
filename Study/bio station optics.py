import json
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import xrt.backends.raycing.materials as rm
from miror_refl_xrt import relf2energy
import xrt.backends.raycing.materials_compounds as xcomp
def main():
    hard=False
    soft2784=False
    soft409=False
    VEPP=True

    qual=1000
    if hard:
        path = 'C:\\Users\\Oleg\\\Desktop\\ВКР\\si_mirror2470.txt'
        data = genfromtxt(path, delimiter=f' ', dtype=float)
        mirror = []
        for j in range(qual + 1):
            mirror.append(data[j][1])
        path = 'C:\\Users\\Oleg\\Desktop\\ВКР\\spectra\\станция биологии\\k hard spectrum after meeting spectrum and aperture-7.json'
        name = f'Mo/B4C'
        mTop = rm.Material('Mo', rho=10.22)
        mBot = xcomp.BoronCarbide()
        mSub = rm.Material('Si', rho=2.32)
        mirrorMulti = relf2energy(np.rad2deg(50.e-3), 52.5, 0.4, mTop, mBot, mSub, name, show=False)
    else:
        path = 'C:\\Users\\Oleg\\\Desktop\\ВКР\\calc_CrSc_independent_0.txt'
        data = genfromtxt(path, delimiter=f' ', dtype=float)
        mirrorObj = []
        for j in range(qual + 1):
            mirrorObj.append(data[j][1])
        if soft2784:
            path = 'C:\\Users\\Oleg\\Desktop\\ВКР\\spectra\\станция биологии\\284 эВ финал 0,375 сигма-28.json'
            name = f'Fe/C'
            mTop = rm.Material('Fe', rho=7.874)
            mBot = rm.Material('C', rho=2.266)
            mSub = rm.Material('Si', rho=2.32)
            mirrorMulti = relf2energy(87, 43.8, 0.3, mTop, mBot, mSub, name, show=False)
        else:
            if soft409:
                path = 'C:\\Users\\Oleg\\Desktop\\ВКР\\spectra\\станция биологии\\409.9 эВ финал 0,375 сигма -32.json'
                name = f'Mo/B4C'
                mTop = rm.Material('Mo', rho=10.22)
                mBot = xcomp.BoronCarbide()
                mSub = rm.Material('Si', rho=2.32)
                mirrorMulti = relf2energy(87, 52.5, 0.4, mTop, mBot, mSub, name, show=False)

    if VEPP:
        path='C:\\Users\\Oleg\\Desktop\\ВКР\\spectra\\VEPP\\spectr_pinhole-7.json'
    with open(path) as f:
        spectra_source = json.load(f)

    source = spectra_source["Output"]["data"][1]
    energy = spectra_source["Output"]["data"][0]
    qual=len(energy)-1


    # path = 'C:\\Users\\Oleg\\\Desktop\\ВКР\\WB4C_mirror2400.txt'
    # data = genfromtxt(path, delimiter=f' ', dtype=float)
    # mirrorMulti = []
    # for j in range(qual + 1):
    #     mirrorMulti.append(data[j][1])
    # print(mirrorMulti)


    # name = f'Mo/B4C'
    # mTop = rm.Material('Mo', rho=10.22)
    # mBot = xcomp.BoronCarbide()
    # mSub = rm.Material('Si', rho=2.32)
    # mirrorMulti=relf2energy(np.rad2deg(50.e-3), 52.5, 0.4, mTop, mBot, mSub, name, show=False)







    filter1=[]
    nmax=0
    for x in range(qual+1):
        if (source[x]==max(source)):
            nmax=x
    for x in range(qual + 1):
        if (max(source)/2<=source[x]) :
            filter1.append(1)
        else:
            filter1.append(0)
    print(filter1)

    if VEPP:
        filterMono=[]
        proc = 1.e-4
        for x in range(qual + 1):
            if (10000*(1+proc) >= energy[x]) and (10000*(1-proc)<= energy[x]):
                filterMono.append(1)
            else:
                filterMono.append(0)
        print(filterMono)
        print(sum(filterMono))

    nphoton=0
    nPower=0
    nPowerHarm = 0
    nPowerSource = 0
    delE=(max(energy)-min(energy))/qual
    print(delE)

    if soft409 or soft2784 or hard:
        if hard:
            beamFirstMirror = []
            beamDMM = []
            beamFinal = []
            for i in range(qual + 1):
                beamFirstMirror.append(source[i]*mirror[i])
                beamDMM.append(source[i]*mirror[i]*mirrorMulti[i])
                beamFinal.append(source[i]*mirror[i]*mirrorMulti[i]*0.3)
                nphoton+=source[i]*mirror[i]*mirrorMulti[i]*0.3*delE
                nPower+=source[i]*mirror[i]*mirrorMulti[i]*0.3*delE*energy[i]
                nPowerHarm += source[i]*filter1[i] * delE * energy[i]


                nPowerSource +=source[i]*delE*energy[i]
            plt.plot(energy, source, label='Источник')
            plt.plot(energy, beamFirstMirror, label='После зеркала ПВО')
            plt.plot(energy, beamDMM, label='После многослойного зеркала')
            plt.plot(energy, beamFinal, label='После FZP')
            plt.title(r'Источник для К края S  2472эВ')
            plt.ylabel(f'{spectra_source["Output"]["titles"][1]} {spectra_source["Output"]["units"][1]}')

        else:
            beamFirstMirror = []
            beamDMM = []
            beamFinal = []
            for i in range(qual + 1):
                beamFirstMirror.append(source[i] * 0.3)
                beamDMM.append(source[i] * 0.3 * mirrorMulti[i] ** 2)
                nphoton += source[i] * 0.3 * mirrorMulti[i] ** 2 * delE
                nPower += source[i] * 0.3 * mirrorMulti[i] ** 2 * delE * energy[i]
                nPowerHarm += source[i]*filter1[i] * delE * energy[i]
                nPowerSource += source[i] * delE * energy[i]
            if soft2784:
                plt.title(r'Источник для К края С  284,2 эВ')
            else:
                plt.title(r'Источник для К края N  409,9 эВ')
            plt.plot(energy, source, label='Источник')
            plt.plot(energy, beamFirstMirror, label='После линзы Брэгга-Френеля')
            plt.plot(energy, beamDMM, label='После объектива Шварцшильда')
        print(f'фотонов {round(nphoton / 10e13, 3)} 10^13')
        print(f'мощность источника {round(nPowerSource * 1.6e-19, 3)} Вт')
        print(f'плотность мощности источника {round(nPowerSource * 1.6e-19 / (np.pi * 0.125 ** 2), 3)} Вт/мм^2')
        print(f'мощность {round(nPower * 1.6e-19 * 1000, 3)} мВт')
        print(f'плотность мощности {round(nPower * 1.6e-19 / (np.pi * 36.6e-6 ** 2) / 1.e6, 3)} МВт/мм^2')
        print(f'мощность гармоники аналит {round(2472 * 16 * 1.e13 * 1.6e-19, 3)} Вт')

    if VEPP:
        beamMono = []
        for i in range(qual + 1):
            beamMono.append(source[i] * filterMono[i])
            nphoton += source[i] * filterMono[i]* delE
            nPower += source[i] * filterMono[i]* delE * energy[i]
            nPowerSource += source[i] * delE * energy[i]
        plt.plot(energy, source, label='Источник')
        plt.plot(energy, beamMono, label=f'dE/E={proc}')
        print(f'фотонов {round(nphoton / 10e9, 3)} 10^9')
        print(f'мощность источника {round(nPowerSource * 1.6e-19*1.e3, 3)} мВт')
        print(f'плотность мощности источника {round(nPowerSource * 1.6e-19 / (np.pi * 0.125 ** 2), 3)} Вт/мм^2')
        print(f'мощность {round(nPower * 1.6e-19 * 1000, 3)} мВт')
        print(f'плотность мощности {round(nPower * 1.6e-19 / (np.pi * 36.6e-6 ** 2) / 1.e6, 3)} МВт/мм^2')
        print(f'мощность гармоники аналит {round(2472 * 16 * 1.e13 * 1.6e-19, 3)} Вт')

    plt.legend(loc='best', fontsize=12)
    plt.xlabel(r'Энергия, эВ')
    plt.yscale('log')
    plt.grid(True)



    plt.show()


if __name__ == '__main__':
    main()