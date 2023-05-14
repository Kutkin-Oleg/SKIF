from numpy import genfromtxt
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

def main():
    path='C:\\Users\\synchrotron\\PycharmProjects\\SKIF\\database\\mirror_refl.csv'
    data = genfromtxt(path, delimiter=';', dtype=float)

    columns=['angle']
    angle=[]
    for i in np.arange(0, len(data), 1):
        angle.append(f'{data[i, 0]} °')
    for i in np.arange(0, len(data[0])-1, 1):
        columns.append(f'{(i+1)*1000} eV')

    df = pd.DataFrame(data=data, columns=columns,  index=angle)
    print(df)
    fig = px.imshow(df, aspect="auto", origin='lower')
    fig.show()

    # path = 'C:\\Users\\synchrotron\\PycharmProjects\\SKIF\\database\\Si_refl.csv'
    # data = genfromtxt(path, delimiter=f'\t', dtype=float)
    # data_tabl = [[0] * 256 for i in range(256)]
    # for j in np.arange(1, 255*255, 1):
    #     data_tabl[int(data[j][0])] [int(data[j][1]) ]=data[j][2]
    # columns = []
    # angle=[]
    # N=256
    # for i in np.arange(0, N, 1):
    #     columns.append(f'{1000+25000/N*i} eV')
    #     angle.append(f'{18 / N * i} mkrad')
    #
    # df = pd.DataFrame(data=data_tabl, columns=columns,  index=angle)
    # print(df)
    # fig = px.imshow(df, aspect="auto", origin='lower')
    # fig.show()






if __name__ == '__main__':
    main()