import matplotlib.patches
import matplotlib.path
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from matplotlib import cm
from matplotlib.ticker import LinearLocator



R=0.1
Step=100
Rparab=2.5
b=0.3
tet=63.42/180*np.pi
a=1/(4*Rparab)

xcircle=[]
ycircle=[]
xlens=[]
ylens=[]

# plt.grid()
axes = plt.gca()
axes.set_aspect("equal")
#границы параболы и центров окружностей
xlim=[0,20]
ylim=[0,20]
# xmap=np.linspace(xlim[0],xlim[1], Step)
# ymap=np.linspace(ylim[0],ylim[1], Step)
xmap=np.arange(xlim[0],xlim[1], 2*R)
ymap = np.arange(ylim[0], ylim[1], 2*R)


Step=len(xmap)

#переводит номер точки массива в координату
def transp(temp, count):
    return(temp[0] + 2*temp[1] /Step * count)

def integrator(numx,numy):
    temp = integrate.quad(lambda x: (R**2+(x-xmap[numx])**2)**0.5, xlim[0], xlim[1])
    return (temp[0])

#условие не пересечения окружностей
def test(numx,numy):
    for i in range(len(xlens)):
        if ((numx-xlens[i])**2+(numy-ylens[i])**2)**0.5<2*R:
            return (False)
    return (True)


middle=(((ylim[1]-ylim[0])**2+(xlim[1]-xlim[0])**2)**0.5*np.sin(tet+np.arctan(xlim[1]/ylim[1])))/2
def parabola(x):
    a = 1 / (4 * Rparab)
    return a*(x-middle)**2+b

def volume_test(testy):
    Vtemp= 2 * R
    for ycircle in ylens:
        if (ycircle + R > testy) and (ycircle - R < testy):
            Vtemp += 2 * (R ** 2 - (testy- ycircle) ** 2) ** 0.5
    testS = 2 * parabola(testy) - Vtemp
    return(abs(testS))

def volume_test_v1_1(testy):
    Vtemp= 2*R
    ylens.append(testy)
    area=[]
    for i in range(Step):
        for ycircle in ylens:
            if (ycircle + R >= ymap[i]) and (ycircle - R <= ymap[i]):
                Vtemp += 2 * (R ** 2 - (ymap[i]- ycircle) ** 2) ** 0.5
        print(Vtemp)
        if (abs(testS[i]) < abs(2 * parabola( ymap[i]) - Vtemp)):
            ylens.pop()
            return (False)
        else:
            testS[i]=abs(2 * parabola(ymap[i]) - Vtemp)
            Vtemp=0
    ylens.pop()
    return (True)

def volume_test_v1_2(testy):
    tempS=2*R

    ylens.append(testy)
    for ii in np.linspace(-R+testy, R+testy,20):
        for ycircle in ylens:
            if (ycircle-R<=ii) and (ycircle+R>=ii):
                tempS+=abs(2*(R**2-(ii-ycircle)**2)**0.5)


    if (abs(testS[i])>=abs(2*parabola(testy-tempS))):
        testS[i]=abs(2*parabola(testy)-tempS)
        tempS = 0
        print(testS[i])
    else:
        ylens.pop()
        return (False)

    ylens.pop()
    return (True)



S=1e3
testS=[]
for x in range(Step):
    # testS.append(2*parabola(ymap[x]))
    testS.append(S)

eventest=0
def create_list_circle():

    for i in range(len(xmap)):
        # if i%2==0:
        #     eventest=1
        # else:
        #     eventest=0
        for j in range(len(ymap)):
            r = (xmap[i] ** 2 + ymap[j] ** 2) ** 0.5
            fi=np.arctan(xmap[i]/ymap[j])
            tempx=(r*np.cos(fi+tet))
            tempy=(r * np.sin(fi+tet))
            # if test(xmap[i],ymap[j]+R*eventest) and (xmap[i]<=parabola(ymap[j]+R*eventest)) and (xmap[i]>=-parabola(ymap[j]+R*eventest)):
            if  (tempx <= parabola(tempy)) and (tempx >= -parabola(tempy)) and (tempy<=middle+4) and (tempy>=middle-4):
            # if (tempx <= 2*parabola(tempy)) and (tempx >=0) and (tempy <= middle + 4) and (
            #             tempy >= middle - 4):
            # if True:
            # if  test(tempx,tempy) and (volume_test_v1_2(tempy)) :
                xlens.append(tempx)
                ylens.append(tempy)
    return (xlens, ylens)




xlens, ylens=create_list_circle()

# for xx in range(len(xlens)):
#     r=(xlens[xx]**2+ylens[xx]**2)**0.5
#     fi=np.arctan(ylens[xx]/xlens[xx])
#     xlens[xx]=(r*np.cos(fi+tet))
#     ylens[xx]=(r * np.sin(fi+tet))

plt.subplot(1, 2, 1)
for i in range(len(xlens)):
    # plt.text(xlens[i], ylens[i], f"{i}", fontsize=5)
    circle = matplotlib.patches.Circle((xlens[i], ylens[i]), radius=R, fill=True)
    plt.gca ().add_artist (circle)

ymap=np.linspace(min(ylens),max(ylens), Step)
xparab=parabola(ymap)
plt.scatter(xlens, ylens, s=1, color='black')
plt.plot(-xparab, ymap, color='r')
plt.plot(xparab, ymap, color='r')
plt.title('угол наклона %.2f°'%(tet*180/np.pi))
# plt.show()



def circle(x, x0):
    return (R**2-(x-x0)**2)**0.5


def my_integrate(f,a,b,dx):
    x=np.arange(a,b,dx)
    y=f(x)
    return (y.sum()-(y[0]+y[-1])/2.)*dx  # we are adding the a


xmap=np.linspace(min(xlens),max(xlens), 10000)
ymap=np.linspace(min(ylens),max(ylens), 10000)

EdgesParabola=[]
EdgesCircles=[]
EdgesDifferrence=[]
temp=0
def second_plot():
    tempEdgesParabola = []
    tempEdgesCircles = []
    tempEdgesDifferrence = []
    temp = 0
    for y in ymap:
        tempEdgesParabola.append(2*parabola(y))
        for ycircle in ylens:
            if (ycircle+R>=y) and (ycircle-R<=y):
                temp+=2*(R**2-(y-ycircle)**2)**0.5
        # print(f'{parabola(y)} {temp}')
        tempEdgesCircles.append(temp)
        tempEdgesDifferrence.append(2*parabola(y)-temp)
        temp=0
    return (tempEdgesParabola, tempEdgesCircles, tempEdgesDifferrence)
def standDev(EdgesCircles, EdgesParabola):
    sumDev=0
    for i in range(len(EdgesCircles)):
        sumDev+=(EdgesCircles[i]-EdgesParabola[i])**2
    return ((sumDev/len(EdgesCircles))**0.5)

def linearDev(EdgesCircles, EdgesParabola):
    sumDev=0
    for i in range(len(EdgesCircles)):
        sumDev+=abs(EdgesCircles[i]-EdgesParabola[i])
    return ((sumDev/len(EdgesCircles)))


EdgesParabola, EdgesCircles, EdgesDifferrence=second_plot()
# EdgesCircles.append(0)
# EdgesParabola.append(0)
# EdgesParabola.append(ylim[1]*2/Step*parabola(ylim[1]))
plt.subplot(1, 2, 2)
# plt.stairs(ymap,EdgesParabola, orientation='vertical', fill=False, baseline=0)
# plt.stairs(ymap,EdgesCircles, orientation='vertical', fill=False, baseline=0)
plt.step(EdgesParabola, ymap)
# plt.step(testS, ymap)
# plt.step(EdgesDifferrence, ymap)
plt.step(EdgesCircles, ymap)
plt.title('радиус параболы %.2f'%(Rparab))
plt.show()




deviation=[]
linDev=[]
angle=np.linspace(0, np.pi/4, 10)
dev2D=[]
linDev2D=[]
parabRadMap=np.linspace(1, 10, 10)

for temprad in parabRadMap:
    Rparab=temprad
    for tempangle in angle:
        xmap = np.arange(xlim[0], xlim[1], 2 * R)
        ymap = np.arange(ylim[0], ylim[1], 2 * R)
        xcircle = []
        ycircle = []
        xlens = []
        ylens = []
        tet=tempangle
        xlens, ylens=create_list_circle()
        xmap = np.linspace(min(xlens), max(xlens), 10000)
        ymap = np.linspace(min(ylens), max(ylens), 10000)
        EdgesParabola, EdgesCircles, EdgesDifferrence = second_plot()
        tempdev=standDev(EdgesCircles, EdgesParabola)
        deviation.append(tempdev)
        linDev.append(linearDev(EdgesCircles, EdgesParabola))


        if False:
            plt.subplot(1, 2, 1)
            for i in range(len(xlens)):
                # plt.text(xlens[i], ylens[i], f"{i}", fontsize=5)
                circle = matplotlib.patches.Circle((xlens[i], ylens[i]), radius=R, fill=True)
                plt.gca().add_artist(circle)
            xparab = parabola(np.linspace(min(ylens), max(ylens), len(xlens)))
            plt.scatter(xlens, ylens, s=1, color='black')
            plt.plot(-xparab, np.linspace(min(ylens), max(ylens), len(ylens)), color='r')
            plt.plot(xparab, np.linspace(min(ylens), max(ylens), len(ylens)), color='r')
            plt.title('угол наклона %.2f°' % (tet * 180 / np.pi))
            # plt.show()

            # EdgesParabola, EdgesCircles, EdgesDifferrence = second_plot()
            plt.subplot(1, 2, 2)
            plt.step(EdgesParabola, ymap)
            plt.step(EdgesCircles, ymap)
            plt.title('Среднеквадратическое отклонение  %.3f' % tempdev)
            plt.show()
        xcircle = []
        ycircle = []
        # print(deviation)
    if False:
        plt.plot(angle, deviation)
        plt.ylabel('Среднеквадратичное отклонение')
        plt.xlabel('Угол')
        plt.show()
        plt.plot(angle, linDev)
        plt.ylabel('Среднее линейное отклонение')
        plt.xlabel('Угол')
        plt.show()
    dev2D.append(deviation)
    linDev2D.append(linDev)
    print(f'При радиусе параболы {Rparab}')
    for i in range(len(deviation)):
        if deviation[i] == min(deviation):
            print(f'при угле {angle[i]} минимальное среднеквадратичное отклонение {min(deviation)}')
    for i in range(len(linDev)):
        if linDev[i] == min(linDev):
            print(f'при угле {angle[i]} минимальное среднее линейное отклонение {min(linDev)}\n')
    deviation=[]
    linDev=[]

# print(dev2D)
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
X, Y = np.meshgrid(angle, parabRadMap)
Z = np.array(dev2D)
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)

ax.set_xlabel('Угол')
ax.set_ylabel('Радиус параболы')
ax.set_zlabel('Среднеквадратичное отклонение')
plt.show()

