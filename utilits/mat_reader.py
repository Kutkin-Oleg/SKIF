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

dir = f'C:\\Users\\synchrotron\\PycharmProjects\\SKIF\\SKIF_NSTU_SCW\\results\\mat'
def find_spot(radius):

    filename = f'C:\\Users\\synchrotron\\PycharmProjects\\SKIF\\SKIF_NSTU_SCW\\results\\mat\\change-screen-{radius}'
    min_x=10e3
    min_y=10e3
    distance=''
    for file in os.listdir(filename):
        if file.endswith(".mat"):
            data = scipy.io.loadmat(filename+'\\'+file)

            # print(file)
            # print(f"Размер по х-{data['dx']}")
            # print(f"Размер по y-{data['dy']}")
            # print(f"Размер пятна-{data['dx']*data['dy']}\n")
            if (data['dx']*data['dy']<min_x*min_y):
                min_x=data['dx']
                min_y=data['dy']
                distance=file

    data = scipy.io.loadmat(filename + '\\' + distance)
    tr, dist = distance.split('_')
    dist = dist.replace('.mat', '')
    print(f'минимальный фокус при экране на {dist} от источника')
    print(f"Размер по х-{data['dx']}")
    print(f"Размер по y-{data['dy']}")
    print(f"Размер пятна-{data['dx'] * data['dy']}\n")
    return ([dist, data['dx'] * data['dy']])

def graph_focus():
    for cat in os.listdir(dir):
        print(cat)

def main():

    # radius = '-140000.0'
    # temp=find_spot(radius)
    # print(temp)

if __name__ == '__main__':
    main()