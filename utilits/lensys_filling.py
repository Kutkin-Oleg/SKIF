import matplotlib.patches
import matplotlib.path
import matplotlib.pyplot as plt
from scipy import integrate

xlim=[-2,2]
ylim=[-2,2]
R=0.3
Step=500

xmap=[]
ymap=[]
xcircle=[]
ycircle=[]
plt.xlim(xlim)
plt.ylim(ylim)
plt.grid()
axes = plt.gca()
axes.set_aspect("equal")
xcircle.append(0)
ycircle.append(0)
circle = matplotlib.patches.Circle((xlim[1], ylim[1]), radius=R, fill=False)
axes.add_patch(circle)

#переводит номер точки в массиве в координату
def transp(temp, count):
    return(temp[0] + 2*temp[1] /Step * count)

def test(numx,numy):
    for i in range(len(xcircle)):
        if ((xmap[numx]-xcircle[i])**2+(ymap[numy]-ycircle[i])**2)**0.5<2*R:
            return (False)
    xcircle.append(xmap[numx])
    ycircle.append(ymap[numy])
    return(True)



for i in range(Step+1):
    xmap.append(transp(xlim, i))
    for j in range(Step+1):
        ymap.append(transp(ylim, j))
        test(i,j)
        # if test(i,j):
            # circle = matplotlib.patches.Circle((xmap[i], ymap[j]), radius=R, fill=False)
            # axes.add_patch(circle)

for i in range(len(xcircle)):
    circle = matplotlib.patches.Circle((xcircle[i], ycircle[i]), radius=R, fill=False)
    axes.add_patch(circle)
plt.show()