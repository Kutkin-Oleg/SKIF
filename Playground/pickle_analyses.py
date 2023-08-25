import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import os
import xraydb
import xrt.backends.raycing.materials as rm


mBeryllium = rm.Material('Be', rho=1.848, kind='lens')
subdir=fr"C:\Users\synchrotron\PycharmProjects\SKIF\results"
yt=1.2e-3
L=270e-3

material='Be'
# density gr/sm^3
density=1.848


leng=[]
tabx=[]
taby=[]
focusEn=[]
focusLen=[]
focusDiff=[]
minx=1e6
minLen=0
focusFormula=[]
for En in os.listdir(subdir):
    focusEn.append(float(En))
    delta = np.real(1. - mBeryllium.get_refractive_index(float(En)))
    for file in os.listdir(os.path.join(subdir, En)):
        if file.endswith(".mat"):
            data = scipy.io.loadmat(subdir+'\\'+En+'\\'+file)
            # print(data)
            el, chan = file.split('_')
            chan=chan.replace('.mat', '' )
            beg, end = chan.split('.')
            # leng.append(int(beg)/1000)
            if data['dx'][0][0]<minx:
                minx=data['dx'][0][0]
                minLen=int(beg)/1000

    temp = xraydb.xray_delta_beta(material, density, float(En))
    focusFormula.append(yt ** 2 / (L * delta))
    tabx.append(minx)
    focusLen.append(minLen-28)
    focusDiff.append(yt ** 2 / (L * delta)-minLen+28)
    minx=1.e3
print(focusEn)
print(focusLen)
print(focusFormula)

plt.grid()
plt.plot(focusEn, focusLen, label='Результат моделирование')
plt.plot(focusEn, focusFormula, label='Расчет по формуле')
plt.plot(focusEn, focusDiff, label='Разность')
plt.ylabel('Lh - расстояние до фокуса, м')
plt.xlabel('Энергия, эВ')
plt.legend(loc='best', fontsize=12)
plt.show()