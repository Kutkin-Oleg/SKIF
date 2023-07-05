from numpy import genfromtxt
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import json


def main():
    path = 'C:\\Users\\synchrotron\\Desktop\\spectra\\results\\SKIF_1-1-1.json'
    with open('C:\\Users\\synchrotron\\Desktop\\spectra\\results\\SKIF_1-1-1.json') as f:
        source= json.load(f)
    # print(source["Output"]["data"][0])
    path = 'C:\\Users\\synchrotron\\Desktop\\1-1_Filters\\refl_oasys\\diamond_0.8mm.txt'
    dataDiamond = genfromtxt(path, delimiter=f'', dtype=float)
    DiamondFilter = []
    FilterEnergy=[]
    for i in range(600):
        DiamondFilter.append(source["Output"]["data"][1][i] * dataDiamond[i][1])
        FilterEnergy.append(dataDiamond[i][0])
    # print(DiamondFilter)
    path = 'C:\\Users\\synchrotron\\Desktop\\1-1_Filters\\refl_oasys\\M0-Be-10.3keV.txt'
    dataMirror = genfromtxt(path, delimiter=f'', dtype=float)
    DiamondMirrorFilter = []
    for i in range(600):
        DiamondMirrorFilter.append(source["Output"]["data"][1][i] * dataMirror[i][1]**2*dataDiamond[i][1])
    path = 'C:\\Users\\synchrotron\\Desktop\\1-1_Filters\\refl_oasys\\Ti_0.015mm.txt'
    dataTi = genfromtxt(path, delimiter=f'', dtype=float)
    DiamondMirrorTiFilter = []
    for i in range(600):
        DiamondMirrorTiFilter.append(source["Output"]["data"][1][i] * dataMirror[i][1] ** 2 * dataDiamond[i][1]*dataTi[i][1])

    path = 'C:\\Users\\synchrotron\\Desktop\\1-1_Filters\\refl_oasys\\Ti_0.05mm.txt'
    dataTi50 = genfromtxt(path, delimiter=f'', dtype=float)
    path = 'C:\\Users\\synchrotron\\Desktop\\1-1_Filters\\refl_oasys\\W-B4C-30.922keV.txt'
    dataMirrorWB4C = genfromtxt(path, delimiter=f'', dtype=float)
    DiamondMirrorWB4CFilter = []
    for i in range(600):
        DiamondMirrorWB4CFilter.append(source["Output"]["data"][1][i] * dataMirrorWB4C[i][1] ** 2 * dataDiamond[i][1])
    DiamondMirrorWB4CTiFilter = []
    for i in range(600):
        DiamondMirrorWB4CTiFilter.append(
            source["Output"]["data"][1][i] * dataMirrorWB4C[i][1] ** 2 * dataDiamond[i][1] * dataTi50[i][1])



    path = 'C:\\Users\\synchrotron\\Desktop\\1-1_Filters\\refl_oasys\\Be-Cr-30.922keV.txt'
    dataMirrorBeCr = genfromtxt(path, delimiter=f'', dtype=float)
    DiamondMirrorBeCrFilter = []
    for i in range(600):
        DiamondMirrorBeCrFilter.append(source["Output"]["data"][1][i] * dataMirrorBeCr[i][1] ** 2 * dataDiamond[i][1])
    DiamondMirrorBeCrTiFilter = []
    for i in range(600):
        DiamondMirrorBeCrTiFilter.append(
            source["Output"]["data"][1][i] * dataMirrorBeCr[i][1] ** 2 * dataDiamond[i][1] * dataTi50[i][1])



    fig = go.Figure()
    fig.add_trace(go.Scatter(x=source["Output"]["data"][0], y=source["Output"]["data"][1], name="Undulator"))
    fig.add_trace(go.Scatter(x=FilterEnergy, y=DiamondFilter, name="Diamond 0.8 mm"))
    fig.add_trace(go.Scatter(x=FilterEnergy, y=DiamondMirrorFilter, name="Diamond 0.8 mm+DMM MoBe"))
    fig.add_trace(go.Scatter(x=FilterEnergy, y=DiamondMirrorTiFilter, name="Diamond 0.8 mm+DMM+Ti 0.015 mm"))

    fig.update_layout(title_text='DMM MoBe', xaxis_title='Energy, eV',
                      yaxis_title='Flux density, ph/s/0.1%B.W.',
    legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.7))
    fig.update_yaxes(type="log", range=[10, 16])
    fig.show()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=source["Output"]["data"][0], y=source["Output"]["data"][1], name="Undulator"))
    fig.add_trace(go.Scatter(x=FilterEnergy, y=DiamondFilter, name="Diamond 0.8 mm"))
    fig.add_trace(go.Scatter(x=FilterEnergy, y=DiamondMirrorWB4CFilter, name="Diamond 0.8 mm+DMM W-B4C"))
    fig.add_trace(go.Scatter(x=FilterEnergy, y=DiamondMirrorWB4CTiFilter, name="Diamond 0.8 mm+DMM+Ti 0.05 mm"))
    fig.update_layout(title_text='DMM W-B4C', xaxis_title='Energy, eV',
                      yaxis_title='Flux density, ph/s/0.1%B.W.',
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="left",
                          x=0.7))
    fig.update_yaxes(type="log", range=[10, 16])
    fig.show()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=source["Output"]["data"][0], y=source["Output"]["data"][1], name="Undulator"))
    fig.add_trace(go.Scatter(x=FilterEnergy, y=DiamondFilter, name="Diamond 0.8 mm"))
    fig.add_trace(go.Scatter(x=FilterEnergy, y=DiamondMirrorBeCrFilter, name="Diamond 0.8 mm+DMM Be-Cr"))
    fig.add_trace(go.Scatter(x=FilterEnergy, y=DiamondMirrorBeCrTiFilter, name="Diamond 0.8 mm+DMM+Ti 0.05 mm"))
    fig.update_layout(title_text='DMM Be-Cr', xaxis_title='Energy, eV',
                      yaxis_title='Flux density, ph/s/0.1%B.W.',
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="left",
                          x=0.7))
    fig.update_yaxes(type="log", range=[10, 16])
    fig.show()








if __name__ == '__main__':
    main()