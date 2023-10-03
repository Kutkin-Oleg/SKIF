import xrt.backends.raycing.materials as rm
import matplotlib.pyplot as plt
import numpy as np

mMolibden = rm.Material('Mo', rho=10.22)
mTantal = rm.Material('Ta', rho=16.65)
mAluminium = rm.Material('Al', rho=2.7)
mCuprum = rm.Material('Cu', rho=8.96)
eN=20
dN=1000
energy=[5000*(n+1) for n in range(eN)]
d=[0.01*(n+1) for n in range(dN)]
d=np.linspace(0.01, 5, dN)
atteMo=[[0 for n in range(dN)] for n in range(eN)]
atteTa=[[0 for n in range(dN)] for n in range(eN)]
atteAl=[[0 for n in range(dN)] for n in range(eN)]
atteCu=[[0 for n in range(dN)] for n in range(eN)]
temp=[]
tempCu=[]
for xx in range(eN):
    # muMo = np.imag(1-mMolibden.get_refractive_index(float(energy[xx])))
    muMo=mMolibden.get_absorption_coefficient(energy[xx])
    # muTa = np.imag(1-mTantal.get_refractive_index(float(energy[xx])))
    muTa = mTantal.get_absorption_coefficient(energy[xx])
    temp.append(round(1/muTa*1.e4,2))
    # muAl = np.imag(1-mAluminium.get_refractive_index(float(energy[xx])))
    muAl = mAluminium.get_absorption_coefficient(energy[xx])
    muCu = mCuprum.get_absorption_coefficient(energy[xx])
    tempCu.append(round(1/muCu*1.e4,2))
    for yy in range(dN):
        atteMo[xx][yy] = np.exp(-muMo * d[yy])
        atteTa[xx][yy] = np.exp(-muTa * d[yy])
        atteAl[xx][yy] = np.exp(-muAl * d[yy])
        atteCu[xx][yy] = np.exp(-muCu * d[yy])
plt.grid()

for xx in range(eN):
    # plt.plot(d, atteMo[xx], 'x', label=f'Mo {energy[xx]} кэВ')
    # plt.plot(d, atteTa[xx],'o', label=f'Ta {energy[xx]} кэВ')
    # plt.plot(d, atteAl[xx], label=f'Al {energy[xx]} кэВ')
    plt.plot(d, atteCu[xx], '-', label=f'Cu {energy[xx]} кэВ')
print(f' Attenuation Length Ta {temp} um')
print(f' Attenuation Length Cu {tempCu} um')
plt.xlabel('толщина пластинки, см')
plt.ylabel('I/I0')
plt.legend(loc='best', fontsize=12)
plt.semilogy ()
plt.ylim(1.e-10, 1.e0)
plt.show()