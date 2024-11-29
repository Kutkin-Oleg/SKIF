import xraydb
import numpy as np
import pandas as pd

import plotly.graph_objects as go
import matplotlib.pyplot as plt

# feature thickness, m
t_feature=10.e-9
# background thickness, m
t_back=10.e-6
# background array thickness, m
t_back_Array=np.linspace(1.e-6,100e-6,300)
# background array thickness, mkm
first_energy_Array=np.linspace(274,544,300)
# feature chemical structure
material_feature='H48.6C32.9N8.9O8.9S0.6'
# density, g/cm^3
density_feature=1.35
# background chemical structure
material_background='H2O1'
# background density, g/cm^3
density_background=1
# Signal-to-noise ratio
SNR=1.2
hc=1239*1.e-9


def first_calc(energy_arroy, thick_back_arroy,  show=True):
    n_average =[]
    dose=[]
    for energy in energy_arroy:
        n_string=[]
        dose_string=[]
        wavelengh = 1239 / energy *1.e-9 # m
        # refractive index Returns:(delta, beta, atlen)
        n_feature = xraydb.xray_delta_beta(material_feature, density_feature, energy)
        n_back = xraydb.xray_delta_beta(material_background, density_background, energy)
        mu_back = 4 * np.pi * n_back[1] / wavelengh
        mu_feature = 4 * np.pi * n_feature[1] / wavelengh
        for thick_back in thick_back_arroy:
            # average photon number
            temp=(SNR**2*wavelengh**2)/(8*np.pi**2*t_feature**2*(n_feature[0]-n_back[0])**2)*np.exp(mu_back*(thick_back-t_feature))
            n_string.append(np.log10(temp))
            dose_string.append(np.log10(temp*energy*mu_feature/(density_feature*1000*t_feature**2)*np.exp(-mu_back*(thick_back-t_feature)/2)*1.6e-19))
            # dose_string.append(np.log10(SNR**2*hc/(2*np.pi*density_feature*1000*t_feature**4)*n_feature[1]/(n_feature[0]-n_back[0])**2*np.exp(mu_back*(thick_back-t_feature)/2)))
        n_average.append(n_string)
        dose.append(dose_string)
    if show:
        df = pd.DataFrame(data=n_average, columns=thick_back_arroy*1.e6, index=energy_arroy)
        df=df.T
        print(df)

        fig = go.Figure(data=go.Contour(z=df, x=energy_arroy, y=t_back_Array*1.e6,  colorscale='Gray', contours=dict(start=7,end=10,size=1)))
        fig.update_layout(title_text=f'Количество фотонов на пиксель log10(n), {t_feature*1.e9} нм протеин в глицерине, SNR={SNR}', xaxis_title='Энергия, эВ',
                          yaxis_title='Толщина образца,мкм')
        fig.show()


        df = pd.DataFrame(data=dose, columns=thick_back_arroy * 1.e6, index=energy_arroy)
        df = df.T
        print(df)

        fig = go.Figure(data=go.Contour(z=df, x=energy_arroy, y=t_back_Array * 1.e6, colorscale='Gray', contours=dict(start=7,end=10,size=1)))
        fig.update_layout(
            title_text=f'Доза на пиксель log10(D), {t_feature * 1.e9} нм протеин в глицерине , SNR={SNR}',
            xaxis_title='Энергия, эВ',
            yaxis_title='Толщина образца,мкм')
        fig.show()
    return 0

def second_calc(t_f, t_b, energy_arroy):
    n_phase = []
    n_abs = []
    for energy in energy_arroy:
        wavelengh = 1239 / energy *1.e-9 # m
        # refractive index Returns:(delta, beta, atlen)
        n_feature = xraydb.xray_delta_beta(material_feature, density_feature, energy)
        n_back = xraydb.xray_delta_beta(material_background, density_background, energy)
        mu_back = 4 * np.pi * n_back[1] / wavelengh
        mu_feature = 4 * np.pi * n_feature[1] / wavelengh
        # average photon number
        temp=(SNR**2*wavelengh**2)/(8*np.pi**2*t_f**2*(n_feature[0]-n_back[0])**2)*np.exp(mu_back*(t_b-t_f))
        n_phase.append((temp))
        temp = (SNR ** 2 * wavelengh ** 2) / (8 * np.pi ** 2 * t_f ** 2 * (n_feature[1] - n_back[1]) ** 2) * np.exp(
            mu_back * (t_b - t_f))
        n_abs.append((temp))
    plt.plot(energy_arroy, n_phase, label='Фазовый контраст')
    plt.plot(energy_arroy, n_abs, label='Абсорбционный контраст')
    plt.xlabel(r'Энергия, эВ')
    plt.ylabel(r'log10(n)')
    plt.title(r'Количество фотонов на пиксель log10(n), 5 нм протеин в воде толщина 20 мкм, SNR=1,2')
    plt.legend(loc='best', fontsize=12)
    plt.yscale('log')
    plt.grid(True)
    plt.show()
e=np.linspace(200, 10000,300)
second_calc(5.e-9, 20.e-6, e)
# first_calc(first_energy_Array, t_back_Array)
