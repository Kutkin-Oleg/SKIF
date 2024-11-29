import xrt.backends.raycing.materials as rm
import matplotlib.pyplot as plt
import numpy as np
import xraydb

mMolibden = rm.Material('Mo', rho=10.22)
mBerilliumn = rm.Material('Be', rho=8.848)
mChromium = rm.Material('Cr', rho=7.19)
mTantal = rm.Material('Ta', rho=16.654)
mAluminium = rm.Material('Al', rho=2.7)
mCuprum = rm.Material('Cu', rho=8.96)
mWolframD10 = rm.Material(['W','Cu'], rho=8)
mWolfram = rm.Material('W', rho=19.25)
eN=1
dN=10
# energy=[10000*(n+1) for n in range(eN)]
energy=np.linspace(6000, 6000, eN)
# energy=[10000,12222,14444,16667,18889,21111,23333,25556,27778,30000]
# d=[0.01*(n+1) for n in range(dN)]
d=np.linspace(3/1.e3, 7/1.e3, dN)
atteMo=[[0 for n in range(dN)] for n in range(eN)]
atteTa=[[0 for n in range(dN)] for n in range(eN)]
atteAl=[[0 for n in range(dN)] for n in range(eN)]
atteCu=[[0 for n in range(dN)] for n in range(eN)]
atteWD10=[[0 for n in range(dN)] for n in range(eN)]
atteW=[[0 for n in range(dN)] for n in range(eN)]
atteFilter=[[0 for n in range(dN)] for n in range(eN)]
temp=[]
tempCu=[]
tempWD10=[]
for xx in range(eN):
    # muMo = np.imag(1-mMolibden.get_refractive_index(float(energy[xx])))
    muMo=mMolibden.get_absorption_coefficient(energy[xx])
    # muTa = np.imag(1-mTantal.get_refractive_index(float(energy[xx])))
    muTa = mTantal.get_absorption_coefficient(energy[xx])
    temp.append(round(1/muTa*1.e4,2))
    # muAl = np.imag(1-mAluminium.get_refractive_index(float(energy[xx])))
    muAl = mAluminium.get_absorption_coefficient(energy[xx])
    muCu = mCuprum.get_absorption_coefficient(energy[xx])
    muWD10 = mWolframD10.get_absorption_coefficient(energy[xx])
    muW = mWolfram.get_absorption_coefficient(energy[xx])
    muCr = mChromium.get_absorption_coefficient(energy[xx])
    muBe = mBerilliumn.get_absorption_coefficient(energy[xx])
    tempCu.append(round(1/muCu*1.e4,2))
    tempWD10.append(round(1/muWD10*1.e4,2))
    for yy in range(dN):
        atteMo[xx][yy] = round(np.exp(-muMo * d[yy]),10)
        atteTa[xx][yy] = round(np.exp(-muTa * d[yy]),100)
        atteAl[xx][yy] = round(np.exp(-muAl * d[yy]),5)
        atteCu[xx][yy] = round(np.exp(-muCu * d[yy]),39)
        atteWD10[xx][yy] = np.exp(-muWD10 * d[yy])
        atteW[xx][yy] =round( np.exp(-muW * d[yy]),8)
        atteFilter[xx][yy] =round( np.exp(-(muCr) * d[yy]),8)
plt.grid()
print(f'd {d}')
print(1/muCr*1.e4/3**0.5)
for i in range(len(d)):
    d[i]=d[i]*1.e4
for xx in range(eN):
    # plt.plot(d, atteMo[xx], '-', label=f'Mo {energy[xx]} эВ')
    # plt.plot(d, atteTa[xx],'-', label=f'Ta {energy[xx]/1.e3} кэВ')
    # plt.plot(d, atteAl[xx], label=f'Al {energy[xx]} эВ')
    # plt.plot(d, atteCu[xx], '-', label=f'Cu {energy[xx]} эВ')
    # plt.plot(d, atteW[xx], '-', label=f'W {energy[xx] / 1.e3} кэВ')
    print(f'energy {energy[xx]}')
    print(f'I/I0 Filter {atteFilter[xx]}')
    plt.plot(d, atteFilter[xx], '-', label=f'Be-Cr {energy[xx]/1.e3} кэВ')
print(f' Attenuation Length Ta {temp} um')
print(f' Attenuation Length Cu {tempCu} um')
print(f' Attenuation Length BD-10 {tempWD10} um')

plt.xlabel('толщина пластинки d, мкм')
plt.ylabel('I/I0')
plt.legend(loc='best', fontsize=12)
plt.semilogy ()
# plt.ylim(1.e-8, 1.e0)
plt.show()


dl=30.e-6
eN=1000
energy=np.linspace(1000, 40000, eN)
atteFilterDl=[]
for e in energy:
    # muCr = mChromium.get_absorption_coefficient(e)
    muCr=xraydb.material_mu('Cr', e)
    atteFilterDl.append(round( np.exp(-(muCr) * dl),8))

plt.plot(energy, atteFilterDl, '-', label='Cr Transmission')
plt.xlabel('энергия, эВ')
plt.ylabel('I/I0')
plt.legend(loc='best', fontsize=12)
plt.semilogy ()
# plt.ylim(1.e-8, 1.e0)
plt.show()