import matplotlib.patches
import matplotlib.path
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate

R=0.05
Step=600
a=0.2
b=0.15

xcircle=[]
ycircle=[]
xlens=[]
ylens=[]

xlim=[-3,3]
ylim=[-3,3]
plt.xlim(xlim)
plt.ylim(ylim)
# plt.grid()
axes = plt.gca()
axes.set_aspect("equal")
#границы параболы и центров окружностей
xlim=[-2,2]
ylim=[-2,2]
xmap=np.linspace(xlim[0],xlim[1], Step)
ymap=np.linspace(ylim[0],ylim[1], Step)

#переводит номер точки массива в координату
def transp(temp, count):
    return(temp[0] + 2*temp[1] /Step * count)

def integrator(numx,numy):
    temp = integrate.quad(lambda x: (R**2+(x-xmap[numx])**2)**0.5, xlim[0], xlim[1])
    return (temp[0])

#условие не пересечения окружностей
def test(numx,numy):
    for i in range(len(xlens)):
        if ((xmap[numx]-xlens[i])**2+(ymap[numy]-ylens[i])**2)**0.5<2*R:
            return (False)
    return (True)

def parabola(x):
    return a*x**2+b

for i in range(Step):
    for j in range(Step):
        if test(i,j) and (xmap[i]<=parabola(ymap[j])) and (xmap[i]>=-parabola(ymap[j])):
            xlens.append(xmap[i])
            ylens.append(ymap[j])

plt.subplot(1, 2, 1)
for i in range(len(xlens)):
    circle = matplotlib.patches.Circle((xlens[i], ylens[i]), radius=R, fill=True)
    plt.gca ().add_artist (circle)


xparab=parabola(ymap)
plt.scatter(xlens, ylens, s=1, color='black')
plt.plot(-xparab, ymap, color='r')
plt.plot(xparab, ymap, color='r')
# plt.show()

EdgesParabola=[]
EdgesCircles=[]
temp=0

def circle(x, x0):
    return (R**2-(x-x0)**2)**0.5


def my_integrate(f,a,b,dx):
    x=np.arange(a,b,dx)
    y=f(x)
    return (y.sum()-(y[0]+y[-1])/2.)*dx  # we are adding the a


for y in ymap:
    EdgesParabola.append(2*parabola(y))
    for ycircle in ylens:
        if (ycircle+R>=y) and (ycircle-R<=y):
            temp+=2*(R**2-(y-ycircle)**2)**0.5
    print(f'{parabola(y)} {temp}')
    EdgesCircles.append(temp)
    temp=0


# EdgesCircles.append(0)
# EdgesParabola.append(0)
# EdgesParabola.append(ylim[1]*2/Step*parabola(ylim[1]))
plt.subplot(1, 2, 2)
# plt.stairs(ymap,EdgesParabola, orientation='vertical', fill=False, baseline=0)
# plt.stairs(ymap,EdgesCircles, orientation='vertical', fill=False, baseline=0)
plt.step(EdgesParabola, ymap)
plt.step(EdgesCircles, ymap)
plt.show()


