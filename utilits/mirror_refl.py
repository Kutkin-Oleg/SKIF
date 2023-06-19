from numpy import genfromtxt
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

def main():
    path = 'C:\\Users\\synchrotron\\PycharmProjects\\SKIF\\database\\Si_refl.csv'
    data = genfromtxt(path, delimiter=f'\t', dtype=float)
    data_tabl = [[0] * 256 for i in range(256)]
    for j in np.arange(1, 255*255, 1):
        data_tabl[int(data[j][0])] [int(data[j][1]) ]=data[j][2]
    columns = []
    angle=[]
    N=256
    for i in np.arange(0, N, 1):
        columns.append(1000+25000/N*i)
        angle.append(18 / N * i)

    df = pd.DataFrame(data=data_tabl, columns=columns,  index=angle)

    fig = px.imshow(df, aspect="auto", origin='lower')
    fig.update_layout(xaxis_title='Энергия эВ',
                      yaxis_title='Угол mrad')
    fig.show()
    data_tabl=[[0] * 256 for i in range(256)]
    for j in np.arange(1, 255*255, 1):
        data_tabl[int(data[j][0])] [int(data[j][1]) ]=data[j][2]*data[j][2]
    df = pd.DataFrame(data=data_tabl, columns=columns, index=angle)
    print(df)
    fig = px.imshow(df, aspect="auto", origin='lower')

    fig.update_layout(xaxis_title='Энергия кэВ',
                      yaxis_title='Угол mrad')
    fig.show()






if __name__ == '__main__':
    main()