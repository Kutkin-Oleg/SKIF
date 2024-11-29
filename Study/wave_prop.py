import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
MashSize=32 #размер сетки квадратный
MashSizeX=3
n1=1.57
n2=1
om_S=0
om_R=-5
lam=1.2e-6

om_S=np.arcsin(np.sin(np.radians(om_S))*n1/n2)
om_R=np.arcsin(np.sin(np.radians(om_R))*n1/n2)
k_1=np.array([ 2*np.pi/lam*np.sin(om_S)/n1, 2*np.pi/lam*np.cos(om_S)/n1,0])
k_2=np.array([ 2*np.pi/lam*np.sin(om_R)/n1, 2*np.pi/lam*np.cos(om_R)/n1,0])
fi_0=0
border=0.33

borderX=[-10.e-6, 10.e-6]
borderY=[-10.e-6, 10.e-6]
borderZ=[-10.e-6, 10.e-6]

arrayX=np.linspace(*borderX, MashSize)
arrayY=np.linspace(*borderY, MashSize)
arrayZ=np.linspace(*borderY, MashSizeX)
wave=np.array([[[0] * MashSize for i in range(MashSize)] for i in range(MashSize)], dtype=float)


class WavePropagete():
    def __init__(self, Ngrid):
        self.Ngrid=Ngrid
        self.border=[-1.e-5, 1.e-5]
        self.arrayMesh=np.linspace(*self.border, Ngrid)
        self.grid=[[0] * Ngrid for i in range(Ngrid)]

    def propagate(self):
        for ii in range(self.Ngrid):
            for jj in range(self.Ngrid):
                r = np.array([self.arrayMesh[ii], self.arrayMesh[jj]])
                self.grid[jj][ii] = sphere_inf(k, r)
        return




def plane(lock, locr):
    return (np.exp(-(-1)**0.5*(np.dot(lock, locr) + fi_0)))

def sphere(lock, locr):
    modr=((locr[0]+max(arrayX))**2+locr[1]**2)**0.5
    modk=(lock[0]**2+lock[1]**2)**0.5
    return (np.cos(modk*modr + fi_0))

def sphere_inf(lock, locr):
    modr=((locr[0])**2+locr[1]**2+locr[2])**0.5
    modk=(lock[0]**2+lock[1]**2+lock[2])**0.5
    return (np.exp((-1)**0.5*(modr*modk+ fi_0)))

def gauss(lock, locr, ii):
    w_0=1
    F=np.arctan(2*arrayX[ii]/((lock[0]**2+lock[1]**2)**0.5*w_0**2))
    w=w_0*(1+((lock[0]**2+lock[1]**2)**0.5*w_0**2/(2*arrayX[ii])))**0.5
    return (w/w_0*np.cos(lock[0]*arrayX[ii]-F)-(locr[0]**2+locr[1]**2)*(1/w**2))

def MyMod(x):
    return ((x[0]**2+x[1]**2+x[2]**2)**0.5)


for ii in range(MashSize):
    for jj in range(MashSize):
        for kk in range(MashSizeX):
            r=np.array([arrayX[ii], arrayY[jj] , arrayZ[kk] ])
            wave[kk][jj][ii] = round((plane(k_1, r) + plane(k_2, r) ) * (
                        plane(k_1, r) + plane(k_2, r)).conjugate(), 5)
            # wave[kk][jj][ii]=round((plane(k_1,r)+plane(k_2,r)+plane(-k_2,r))*(plane(k_1,r)+plane(k_2,r)+plane(-k_2,r)).conjugate(),5)
            # wave[kk][jj][ii]=round(sphere_inf(k_1,r),5)

class PhaseBoundary:
    x=100
    n=1.5

maxV=0


for ii in range(MashSize):
    for jj in range(MashSize):
        for kk in range(MashSizeX):
            wave[kk][jj][ii]=((wave[kk][jj][ii]))
            if ((wave[kk][jj][ii])> maxV):
                maxV = wave[kk][jj][ii]
print(maxV)


nColor=8
NewWave1=np.array([[[0] * MashSize for i in range(MashSize)] for i in range(MashSizeX)], dtype=bool)
NewWave2=np.array([[[0] * MashSize for i in range(MashSize)] for i in range(MashSizeX)], dtype=bool)
NewWave3=np.array([[[0] * MashSize for i in range(MashSize)] for i in range(MashSizeX)], dtype=bool)
NewWave4=np.array([[[0] * MashSize for i in range(MashSize)] for i in range(MashSizeX)], dtype=bool)
NewWave5=np.array([[[0] * MashSize for i in range(MashSize)] for i in range(MashSizeX)], dtype=bool)
NewWave6=np.array([[[0] * MashSize for i in range(MashSize)] for i in range(MashSizeX)], dtype=bool)
NewWave7=np.array([[[0] * MashSize for i in range(MashSize)] for i in range(MashSizeX)], dtype=bool)
NewWave8=np.array([[[0] * MashSize for i in range(MashSize)] for i in range(MashSizeX)], dtype=bool)

for ii in range(MashSize):
    for jj in range(MashSize):
        for kk in range(MashSizeX):
            if  (wave[kk][jj][ii]<maxV/nColor):
                NewWave1[kk][jj][ii]=True
            else:
                NewWave1[kk][jj][ii]=False
            if  (wave[kk][jj][ii]>=maxV/nColor) and (wave[kk][jj][ii]<2*maxV/nColor):
                NewWave2[kk][jj][ii]=True
            else:
                NewWave2[kk][jj][ii]=False
            if  (wave[kk][jj][ii]>=2*maxV/nColor) and (wave[kk][jj][ii]<3*maxV/nColor):
                NewWave3[kk][jj][ii]=True
            else:
                NewWave3[kk][jj][ii]=False
            if  (wave[kk][jj][ii]>=3*maxV/nColor) and (wave[kk][jj][ii]<4*maxV/nColor):
                NewWave4[kk][jj][ii]=True
            else:
                NewWave4[kk][jj][ii]=False
            if  (wave[kk][jj][ii]>=4*maxV/nColor) and (wave[kk][jj][ii]<5*maxV/nColor):
                NewWave5[kk][jj][ii]=True
            else:
                NewWave5[kk][jj][ii]=False
            if  (wave[kk][jj][ii]>=5*maxV/nColor) and (wave[kk][jj][ii]<6*maxV/nColor):
                NewWave6[kk][jj][ii]=True
            else:
                NewWave6[kk][jj][ii]=False
            if  (wave[kk][jj][ii]>=6*maxV/nColor) and (wave[kk][jj][ii]<7*maxV/nColor):
                NewWave7[kk][jj][ii]=True
            else:
                NewWave7[kk][jj][ii]=False
            if  (wave[kk][jj][ii]>=7*maxV/nColor):
                NewWave8[kk][jj][ii]=True
            else:
                NewWave8[kk][jj][ii]=False

x,y,z=np.indices((MashSize,MashSize,MashSizeX))
cube=(x>=0)&(y>=0)&(z>=0)

# colNum=10
# intrange=np.linspace(0,maxV, colNum)
# print(intrange)
# voxels=cube
# colors=np.empty(voxels.shape, dtype=object)
#
# def comparater(step1, step2):
#     CNewWave = np.array([[[0] * MashSize for i in range(MashSize)] for i in range(MashSize)], dtype=bool)
#     for ii in range(MashSize):
#         for jj in range(MashSize):
#             for kk in range(MashSize):
#                 if (wave[kk][jj][ii]>=step1) and (wave[kk][jj][ii]<step2):
#                     CNewWave[kk][jj][ii] = True
#                 else:
#                     CNewWave[kk][jj][ii] = False
#     return CNewWave,
# for ii in range(colNum):
#     m,c=comparater(intrange[ii], intrange[ii+1])


voxels=NewWave1|NewWave2|NewWave3|NewWave4|NewWave5|NewWave6|NewWave7|NewWave8
print(voxels)
colors=np.empty(voxels.shape, dtype=object)
colors[NewWave1]='#000000'
colors[NewWave2]='#3f3f3f'
colors[NewWave3]='#6a6a6a'
colors[NewWave4]='#686868'
colors[NewWave5]='#787878'
colors[NewWave6]='#949494'
colors[NewWave7]='#bdbebd'
colors[NewWave8]='#d3d3d3'
print(colors)
fig, ax=plt.subplots(subplot_kw={"projection": "3d"})
ax.voxels(voxels, facecolors=colors,  edgecolor='none', shade=False)
ax.set(xlabel='x, мкм', ylabel='z, мкм', zlabel='y, мкм')
texts=[]

for ii in range(nColor):
    texts.append(f'{round(maxV/nColor*ii/4,3)}-{round(maxV/nColor*(ii+1)/4,3)}')

# plt.legend(texts)

colors = ['#000000', '#3f3f3f','#6a6a6a','#686868','#787878','#949494','#bdbebd','#d3d3d3']

patches = [ plt.plot([],[], marker="o", ms=10, ls="", mec=None, color=colors[i],
            label="{:s}".format(texts[i]) )[0]  for i in range(len(texts)) ]
plt.legend(handles=patches, bbox_to_anchor=(-0.35, 0), loc='lower left', ncol=1, numpoints=1 )

array1=np.linspace(0,MashSize, 5)
array2=np.linspace(-10,10, 5)
plt.yticks(array1, array2)

ax.set_zticks(array1)
ax.set_zticklabels(array2)

array1=np.linspace(0,MashSizeX, 5)
plt.xticks(array1, array2)
plt.show()