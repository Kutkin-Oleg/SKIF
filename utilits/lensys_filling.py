import matplotlib.patches
import matplotlib.path
import matplotlib.pyplot as plt
from scipy import integrate


R=0.05
Step=1000
a=0.5
b=0.25

xmap=[]
ymap=[]
xcircle=[]
ycircle=[]
xcircle.append(-100)
ycircle.append(-100)
xlens=[]
ylens=[]
xlens.append(-5)
ylens.append(-5)

xlim=[-3,3]
ylim=[-3,3]
plt.xlim(xlim)
plt.ylim(ylim)
# plt.grid()
axes = plt.gca()
axes.set_aspect("equal")
xlim=[-2,2]
ylim=[-2,2]


#переводит номер точки в массиве в координату
def transp(temp, count):
    return(temp[0] + 2*temp[1] /Step * count)

def integrator(numx,numy):
    temp = integrate.quad(lambda x: (R**2+(x-xmap[numx])**2)**0.5, xlim[0], xlim[1])
    return (temp[0])

def test(numx,numy):
    for i in range(len(xlens)):
        if ((xmap[numx]-xlens[i])**2+(ymap[numy]-ylens[i])**2)**0.5<2*R:
            return (False)
    return (True)

def parabola(x):
    return a*x**2+b

for i in range(Step+1):
    xmap.append(transp(xlim, i))
    for j in range(Step+1):
        ymap.append(transp(ylim, j))
        if test(i,j) and (xmap[i]<=parabola(ymap[j])) and (xmap[i]>=-parabola(ymap[j])):
            xlens.append(xmap[i])
            ylens.append(ymap[j])


for i in range(len(xlens)):
    circle = matplotlib.patches.Circle((xlens[i], ylens[i]), radius=R, fill=True)
    axes.add_patch(circle)
plt.show()