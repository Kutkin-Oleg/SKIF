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
    qual=255
    name='5 мкм Ti'
    name_path='C:\\Users\\synchrotron\\Desktop\\spectra\\1-1\\diff_thick\\'
    path = name_path+'SKIF_1-1_Diamond.json'
    with open(path) as f:
        spectra_first = json.load(f)
    path = name_path+'SKIF_1-1_Diamond_Ti_5um-1.json'
    with open(path) as f:
        spectra_second = json.load(f)
    # print(spectra["Output"]["data"][0]
    data_first = [[0] * qual for i in range(qual)]
    data_second = [[0] * qual for i in range(qual)]
    data_filter = [[0] * qual for i in range(qual)]
    x=[]
    y=[]
    AbsPower=0
    for i in range(qual):
        x.append(spectra_first["Output"]["data"][0][i])
        y.append(spectra_first ["Output"]["data"][1][i])
        for j in range(qual):
            data_filter[i][j] = (spectra_first["Output"]["data"][3][j + qual * i] - spectra_second["Output"]["data"][3][
                j + qual * i])/(len)**2*1000
            AbsPower=AbsPower+data_filter[i][j]
            data_first[i][j] = (spectra_first["Output"]["data"][3][j + qual * i])/(len)**2
            data_second[i][j]=(spectra_second["Output"]["data"][3][j+qual*i])/(len)**2

    print(AbsPower*(x[0]/(qual/2))**2)
    # print(spectra_Diamond["Output"]["data"][3])




    df = pd.DataFrame(data=data_filter, columns=x,  index=y)

    # print(df)
    fig = px.imshow(df, aspect="auto", origin='lower')
    fig.update_layout(title_text=f'{name}, Вт/мм^2. P(abs) {round(AbsPower*(x[0]/(qual/2))**2, 3)}Вт',xaxis_title='X, мм',
                      yaxis_title='Y, мм', font_size=24)
    fig.show()
    fig.write_image(name_path + f"{name}.png")
    fig = go.Figure()
    fig.update_layout(
        title_text=f'Поглощение {name}, Вт/мм^2. интеграл мощности {round(AbsPower * (x[0] / (qual / 2)) ** 2, 3)} Вт',
        xaxis_title='X, мм',
        yaxis_title='Y, мм')
    fig.add_trace(go.Contour(z=df, x=x, y=y))
    fig.show()


    with open(name_path+f'{name}.txt', 'w') as f:
        f.write('x z W/mm^2')
        f.write('\n')
        for i in range(qual):
            for j in range(qual):
                f.write(f'{x[i]} {y[j]} {data_filter[i][j]}')
                f.write('\n')

    # df = pd.DataFrame(data=data_Diamond, columns=x,  index=y)
    # # print(df)
    # # fig = px.imshow(df, aspect="auto", origin='lower')
    # # fig.update_layout(title_text='Спектр после алмаза алмаза 800 мкм', xaxis_title='X, мм',
    # #                   yaxis_title='Y, м')
    # # fig.show()
    # fig = go.Figure()
    #
    # fig.add_trace(go.Contour(z=df, x=x, y=y))
    # fig.show()
    #
    # df = pd.DataFrame(data=data_Clear, columns=x, index=y)
    # # print(df)
    # # fig = px.imshow(df, aspect="auto", origin='lower')
    # # fig.update_layout(title_text='Спектр после 0,8мм алмаза и 0,0002 титана', xaxis_title='X, мм',
    # #                   yaxis_title='Y, м')
    # # fig.show()
    # fig = go.Figure()
    #
    # fig.add_trace(go.Contour(z=df, x=x, y=y))
    # fig.show()
if __name__ == '__main__':
    main()