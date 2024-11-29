from numpy import genfromtxt
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import json


def main():
    len=20
    qual=255
    name='115 мм  аэрогеля С75% O25% rho=18мг/см³'
    # name='0.8 мм алмаза '

    path = 'C:\\Users\\Oleg\\Desktop\\ВКР\\spectra\\SKIF_1-1_Aerogel_map_115mm-4.json'
    with open(path) as f:
        spectra_1 = json.load(f)
    path = 'C:\\Users\\Oleg\\Desktop\\ВКР\\spectra\\1-1\\3-layers\\glassy carbon\\1-54-2.json'
    with open(path) as f:
        spectra_2= json.load(f)
    # print(spectra["Output"]["data"][0])
    data_1 = [[0] * qual for i in range(qual)]
    data_2 = [[0] * qual for i in range(qual)]
    data_0 = [[0] * qual for i in range(qual)]
    x=[]
    y=[]
    AbsPower=0
    for i in range(qual):
        x.append(spectra_1["Output"]["data"][0][i])
        y.append(spectra_1["Output"]["data"][1][i])
        for j in range(qual):
            # data_1[i][j] = (spectra_1["Output"]["data"][3][j + qual * i] + spectra_1["Output"]["data"][4][
            #     j + qual * i]) / (len) ** 2 * 1000
            # data_0[i][j] = (spectra_1["Output"]["data"][4][j + qual * i] ) / (len) ** 2 * 1000
            data_1[i][j] = (spectra_1["Output"]["data"][2][j + qual * i] - spectra_1["Output"]["data"][3][
                j + qual * i])/((len)**2)*1000
            # data_1[i][j] = (spectra_1["Output"]["data"][3][j + qual * i] ) / ((len) ** 2) * 1000
            AbsPower=AbsPower+data_1[i][j]
            # data_2[i][j] = (spectra_1["Output"]["data"][2][j + qual * i])/(len)**2
            # data_0[i][j]=(spectra_2["Output"]["data"][3][j+qual*i])/(len)**2*1000

    print(AbsPower*(x[0]/(qual/2))**2)
    print(max(max(data_1)))
    # print(spectra_Diamond["Output"]["data"][3])




    df = pd.DataFrame(data=data_1, columns=x,  index=y)

    # print(df)
    # fig = px.imshow(df, aspect="auto", origin='lower')
    # fig.update_layout(title_text=f'Поглощение {name}, Вт/мм^2. интеграл мощности {round(AbsPower*(x[0]/(qual/2))**2, 3)} Вт',xaxis_title='X, мм',
    #                   yaxis_title='Y, мм')
    # fig.update_layout(
    #     xaxis_title='X, мм',
    #     yaxis_title='Y, мм')
    # fig.show()
    # # fig.write_image(f"C:\\Users\\Oleg\\Desktop\\ВКР\\spectra\\углерод\\{name}.png")

    # fig.update_layout(xaxis_title='X, мм',
    #                   yaxis_title='Y, мм',coloraxis_colorbar=dict(title='Вт/мм²'))

    # fig.add_trace(go.Contour(z=df, x=x, y=y))
    # fig.write_image(f"C:\\Users\\Oleg\\Desktop\\ВКР\\картинки\\послестеклоуглерода.png")
    # fig.show()
    fig = go.Figure(data=go.Heatmap(colorbar={"title": "Вт/мм²"},
                                    z=df, x=x, y=y))
    fig.update_layout(title_text=f'{name}',xaxis_title='X, мм',yaxis_title='Y, мм',font=dict(size=30))
    # fig.write_image(f"C:\\Users\\Oleg\\Desktop\\ВКР\\картинки\\0,5стеклоуглерод.png")
    fig.show()
    # with open(f'C:\\Users\\synchrotron\\Desktop\\spectra\\1-1\\{name}.txt', 'w') as f:
    #     f.write('x z W/mm^2')
    #     f.write('\n')
    #     for i in range(qual):
    #         for j in range(qual):
    #             f.write(f'{x[i]} {y[j]} {data_Ti[i][j]}')
    #             f.write('\n')

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