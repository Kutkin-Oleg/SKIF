import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import json


def main():
    len=26.5
    qual=255
    name='Карта поглощения алмаза'
    path = 'C:\\Users\\Oleg\\Desktop\\ВКР\\spectra\\1-1\\diff_thick\\SKIF_1-1_Diamond.json'
    with open(path) as f:
        spectra_Diamond = json.load(f)
    data_Diamond = [[0] * qual for i in range(qual)]
    x=[]
    y=[]
    AbsPower=0
    for i in range(spectra_Diamond["Input"]["Configurations"]["Points (x)"]):
        x.append(spectra_Diamond["Output"]["data"][0][i])
        y.append(spectra_Diamond["Output"]["data"][1][i])
        for j in range(spectra_Diamond["Input"]["Configurations"]["Points (y)"]):
            data_Diamond[i][j] = (spectra_Diamond["Output"]["data"][3][j + qual * i]) / (len) ** 2

    # print(spectra_Diamond["Output"]["data"][3])



    df = pd.DataFrame(data=data_Diamond, columns=x,  index=y)
    # print(df)
    fig = px.imshow(df, aspect="auto", labels=dict(color=f"Вт/мм²"),origin='lower')
    fig.update_layout( xaxis_title='X, мм',
                      yaxis_title='Y, мм',    font=dict(
        size=18,
    ))
    fig.show()
    # fig.write_image(f"C:\\Users\\Oleg\\Desktop\\{name}.png")
    fig.to_image(format="png", engine="kaleido")
    fig.write_image(f"C:\\Users\\Oleg\\Desktop\\ВКР\\картинки\\{name}.png")
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