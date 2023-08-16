import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import os
import xraydb
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
minx=1e6
minLen=0
focusFormula=[]
for En in os.listdir(subdir):
    focusEn.append(float(En))
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
    focusFormula.append(yt ** 2 / (L * temp[0]))
    tabx.append(minx)
    focusLen.append(minLen)
print(focusEn)
print(focusLen)
print(focusFormula)
plt.plot(focusEn, focusLen)
plt.plot(focusEn, focusFormula)

plt.show()