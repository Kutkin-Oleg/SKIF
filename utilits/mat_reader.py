import numpy as np
import cmath
import plotly.graph_objects as go
import plotly.express as px
import math
import pandas as pd
import scipy.io
import matplotlib.pyplot as plt
import os



def heat():
    filename = 'C:\\Users\\synchrotron\\Desktop\\NSU-station\\9kev\\frontend_aperture_total.mat'
    data = scipy.io.loadmat(filename)

    heat2D=data['total2D']
    heat=sum(heat2D)

    X=data['xbinEdges']
    Y=data['ybinEdges']
    x=X[0]
    y=Y[0]
    plt.subplot(223)
    plt.imshow(data['total2D'])

    plt.subplot(224)
    plt.imshow(data['etotal1D_RGB'])

    plt.colorbar()
    plt.show()

    true_power=data['power'][0][0]
    print(data)


radi=''
E0 = 30000
dir=rf"C:\Users\synchrotron\PycharmProjects\SKIF\SKIF_NSTU_SCW\results\mat\{E0}\R-R"

def find_spot(cat, show=False):
    filename=dir+'\\'+cat
    rad = cat.replace('change-screen-', '')

    min_x=10e3
    min_y=10e3
    distance=''
    for file in os.listdir(filename):
        if file.endswith(".mat"):
            data = scipy.io.loadmat(filename+'\\'+file)

            if (float(data['dy'])<min_y):
                min_x=data['dx']
                min_y=data['dy']
                distance=file

    data = scipy.io.loadmat(filename + '\\' + distance)
    tr, dist = distance.split('_')
    dist = dist.replace('.mat', '')
    if show:
        print(f'изгиб {rad}')
        print(f'минимальный фокус при экране на {dist} от источника')
        print(f"Размер по х-{data['dx']}")
        print(f"Размер по y-{data['dy']}")
        print(f"Размер пятна-{data['dx'] * data['dy']}\n")
    return ([float(rad), float(dist), float( data['dy'])])

def graph_focus():
    gra_data=[]
    for cat in os.listdir(dir):
        if cat.startswith('change'):
            gra_data.append(find_spot(cat))
    # gra_data=[ радиус изгиба, расположение экрана где мин пятно, минимальное пятно]
    x=[]
    y=[]
    z=[]
    for i in np.arange(0 ,len(gra_data),1):
        x.append(gra_data[i][0])
        y.append(gra_data[i][1])
        z.append(gra_data[i][2])

    fig = px.scatter(x=x, y=y, title="фокусное расстояние от изгиба")
    fig.update_layout(xaxis_title='Радиус изгиба',
                   yaxis_title='Фокусное расстояние')
    fig.show()
    fig = px.scatter(x=x, y=z, title="мин пятно от изгиба" )
    fig.update_layout(xaxis_title='Радиус изгиба',
                   yaxis_title='Размер пятна')


    fig.show()



def main():
    graph_focus()
    # radius = '-140000.0'
    # temp=find_spot(radius)
    # print(temp)

if __name__ == '__main__':
    main()