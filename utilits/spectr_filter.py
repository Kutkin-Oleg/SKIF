from numpy import genfromtxt
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt

def main():
    path = 'C:\\Users\\Oleg\\Desktop\\ВКР\\spectra\\esrf-5.json'
    with open(path) as f:
        source= json.load(f)
    path = 'C:\\Users\\Oleg\\Desktop\\ВКР\\spectra\\skif-5.json'
    with open(path) as f:
        source2 = json.load(f)
    # print(source["Output"]["data"][0])
    fig = plt.figure(figsize=(10, 5))

    ax = fig.add_subplot(1, 1, 1)
    # ax.semilogy(source["Output"]["data"][0], source["Output"]["data"][1], color='tab:blue', label='ESRF')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    # ax.semilogy(source2["Output"]["data"][0], source2["Output"]["data"][1], color='tab:orange', label="СКИФ")
    plt.plot(source["Output"]["data"][0], source["Output"]["data"][1], color='tab:blue', label='ESRF-EBS')
    plt.plot(source2["Output"]["data"][0], source2["Output"]["data"][1], color='tab:orange', label="СКИФ")
    plt.xlabel(r'Энергия, эВ', fontsize=28)
    plt.ylabel('Спектральная плотность \nпотока, ф/(с∙0.1%E)', fontsize=25)

    plt.legend(loc='upper right', fontsize=12)
    # plt.axis([1000, 32000, 10.e7, 10.e16])

    # plt.savefig('C:\\Users\\Oleg\\Desktop\\ВКР\\картинки\\spectr.png')
    plt.show()

    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=source["Output"]["data"][0], y=source["Output"]["data"][1], name="Без фильтра"))
    # fig.add_trace(go.Scatter(x=source["Output"]["data"][0], y=source["Output"]["data"][5], name="Алмаз 0.8 мм"))
    #
    # fig.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#ffffff', hoverlabel_bordercolor='#000000')
    # fig.update_layout( xaxis_title='Энергия, эВ',
    #                   yaxis_title='Спектральная плотность потока, ф/с(0.1%E)',
    # legend=dict(
    # yanchor="top",
    # y=0.99,
    # xanchor="left",
    # x=0.7))
    # fig.update_yaxes(type="log", range=[8, 16])
    # fig.show()










if __name__ == '__main__':
    main()