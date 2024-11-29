from numpy import genfromtxt
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import json


def main():
    len=26.5
    qual=41
    thic=50.e-6
    name=f'{thic*1.e6}nm angle 30'
    path = 'C:\\Users\\synchrotron\\Desktop\\spectra\\1-1\\incline\\50nmTi0-1.json'
    with open(path) as f:
        spectra_Ti = json.load(f)
    data_Ti = [[0] * qual for i in range(qual)]
    x=[]
    y=[]
    AbsPower=0
    for i in range(qual):
        x.append(spectra_Ti["Output"]["data"][0][i])
        y.append(spectra_Ti["Output"]["data"][1][i])
        for i in range(qual):
            for j in range(qual):
                data_Ti[i][j] =(spectra_Ti["Output"]["data"][3][
                        (j + qual * i)])*max(spectra_Ti["Output"]["data"][2])
    q=0
    for i in range(qual):
        for j in range(qual):
            q=q+data_Ti[i][j]*x[0]*y[0]/(qual/2)**2
    print(q*x[0]*y[0]/(qual/2)**2)
    for ii in spectra_Ti["Output"]["data"][3]:
        AbsPower=AbsPower+ii

    TotalPower=AbsPower*x[0]*y[0]/(qual/2)**2*max(spectra_Ti["Output"]["data"][2])/2
    print(TotalPower)

    df = pd.DataFrame(data=data_Ti, columns=x,  index=y)

    # print(df)
    fig = px.imshow(df, aspect="auto", origin='lower')
    fig.update_layout(title_text=f'Поглощение {name}, Вт/мм^2. интеграл мощности {round(TotalPower, 3)} Вт',xaxis_title='X, мм',
                      yaxis_title='Y, мм')
    fig.show()
    if False:
        fig.write_image(f"C:\\Users\\synchrotron\\Desktop\\spectra\\1-1\\{name}.png")
    fig = go.Figure()
    fig.add_trace(go.Contour(z=df, x=x, y=y))
    fig.show()

    if False:
        with open(f'C:\\Users\\synchrotron\\Desktop\\spectra\\1-1\\{name}.txt', 'w') as f:
            f.write('x z W/mm^2')
            f.write('\n')
            for i in range(qual):
                for j in range(qual):
                    f.write(f'{x[i]} {y[j]} {data_Ti[i][j]}')
                    f.write('\n')

if __name__ == '__main__':
    main()