import numpy as np
import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import json
me=9.1e-31
# Ek=10e6
c=2.99792458e8
x=115
z=6*0.75+8*0.25
rho=0.018
A=12*0.75+16*0.25
# I=1.e-3
nA=6.022e23
Ep=me*c**2/1.60218e-19
targetW=143.13


qualE=255
qualC=1000
energy = np.linspace(0.4e6, 2e6, qualE)
current = np.linspace(0.1e-3, 20e-3, qualC)
Wmap=[[0] * qualE for i in range(qualC)]
WElmap=[[0] * qualE for i in range(qualC)]
dedx=[0] * qualE

path = 'C:\\Users\\Oleg\\Desktop\\ВКР\\spectra\\SKIF_1-1_Aerogel_map_clear-13.json'
with open(path) as f:
    spectra_1 = json.load(f)
data_1=[]

for zz in range(255):
    data_1.append(spectra_1["Output"]["data"][3][(9)*zz+5])

print(f'Энергия покоя {round(Ep*1e-6,3)} МэВ \n')

def ion_loss_calc(Ek, show=False):
    a = Ek / Ep
    beta = (a ** 2 + 2 * a) / (a ** 2 + 2 * a + 1)
    dEheav = 3.1e5 * rho * z / (A * beta) * (11.2 + np.log(beta / (z * (1 - beta))) - beta)
    dEalt = 4 * np.pi / beta * nA * z / A * rho * (2.8e-13) ** 2 * Ep * (
            np.log(2 * Ep * beta / (13.5 * z)) - np.log(1 - beta) - beta)
    dEel = 2 * np.pi / beta * nA * z / A * rho * (2.8e-13) ** 2 * Ep * (
            np.log(Ep * beta * Ek / (2 * (13.5 * z) ** 2 * (1 - beta ** 0.5) ** 2)) - np.log(2) * (
            2 * (1 - beta) ** 0.5 - 1 + beta) + 1 - beta + 1 / 8 * (1 - (1 - beta) ** 0.5) ** 2)

    if show:
        print(f'Кинетическая энергия {round(Ek * 1e-6, 3)} МэВ')
        print(f'релятивистская кинетическая энергия {round(Ep * 1e-6 * ((1 - beta) ** -0.5 - 1), 3)} МэВ')
        print(f'Полная энергия {round(Ep * 1e-6 / (1 - beta) ** 0.5, 3)} МэВ')
        print(f'beta={beta}')
        print(f'a={a}')
    return [dEheav, dEalt, dEel]


def map_ion(show=False):

    for xx in range(qualE):

        Ek=energy[xx]
        dE = ion_loss_calc(Ek)
        dedx[xx]=dE[2]/ 1.e3
        for yy in range(qualC):
            I=current[yy]

            Wheav=x*I*dE[1]/1.6e-19*1.6e-19
            Wel=x*I*dE[2]/1.6e-19*1.6e-19
            Wmap[yy][xx]=Wheav
            WElmap[yy][xx]=Wel

            if show==True:
                print(f'Ток {round(I * 1.e3, 3)} мА')
                print(f'Уд. ион. потери {round(dE[0] / 1.e6, 3)} МэВ/см')
                print(f'Уд. ион. потери алт. {round(dE[1]/ 1.e6, 3)} МэВ/см')
                print(f'Уд. ион. потери эл. {round(dE[2]/ 1.e6, 3)} МэВ/см')
                print(f'Рассеиваемая мощность {round(Wheav , 3)} Вт')
                print(f'Рассеиваемая мощность электрона {round(Wel, 3)} Вт \n')
    return [Wmap,  WElmap, dedx]

def ion_loss_thic(Ek, I):
    delE=[0,0,0]
    loss=[]
    Estr=[]
    for xx in np.linspace(0, x, 255):
        Ek=Ek-delE[2]*x/255
        delE =ion_loss_calc(Ek)
        Estr.append(delE[2]/(1.5**2)/10*I)
        # loss.append(round(delE[2]*x/255*I, 3))
        loss.append(delE[2] * x / 255 * I)

    return [loss,Estr]



def first_calc(show=True, diver=0.05):
    W=map_ion()
    # print(Wmap)
    df = pd.DataFrame(data=W[1], columns=energy*1.e-6,  index=current*1.e3)
    fig = go.Figure(data=go.Heatmap(colorbar={"title": "Вт"},
                                        z=df, x=energy*1.e-6, y=current*1.e3))
    fig.update_layout(title_text=f'Зависимость поглощения {x} см углерода от энергии и тока',xaxis_title='E, МэВ',yaxis_title='I, мА',font=dict(size=30))

    # print(df)

    # plt.plot(energy, Wmap[0]/current[0]/x*1.6e-19/1.6e-12, label=f'Поглощение при {current[0]} мА')
    plt.plot(energy*1.e-6, W[2])
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Энергия, МэВ', fontsize=16)
    plt.ylabel('Ионизационные потери, кэВ/см', fontsize=16)
    # plt.legend()
    Wcr=W[1]


    for xx in range(qualE):
        for yy in range(qualC):
            if (round(Wcr[yy][xx],3)>=targetW*(1-diver)) and (round(Wcr[yy][xx],3)<=targetW*(1+diver)) and False:
                print(f'W={round(Wcr[yy][xx],3)} Вт при E={round(energy[xx]*1.e-6,3)} МэВ I={round(current[yy]*1.e3,3)} мА')
            if (round(Wcr[yy][xx],3)>=targetW*(1-diver)) and (round(Wcr[yy][xx],3)<=targetW*(1+diver)) and True:
                print(f'W={round(Wcr[yy][xx],3)} Вт при E={round(energy[xx]*1.e-6,3)} МэВ I={round(current[yy]*1.e3,3)} мА')
    if show:
        fig.show()
        plt.show()
    return 0

# first_calc()

def second_calc(Ek, I):
    carrage=ion_loss_thic(Ek, I)
    plt.plot(np.linspace(0, x*10, 255), carrage[0])

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Длина пробега, мм', fontsize=16)
    plt.ylabel('Ионизационные потери, Вт', fontsize=16)
    plt.show()


    plt.plot(np.linspace(0, x*10, 255), carrage[1], label=f'Поток электронов I={I*1.e3} мА E={Ek*1.e-6} МэВ')
    plt.plot(np.linspace(0, x * 10, 255), data_1, label='Поток фотонов')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Длина пробега, мм', fontsize=16)
    plt.ylabel('Плотность поглощаемой мощности, Вт/мм³', fontsize=16)
    # plt.title(f'')
    plt.legend(fontsize=14)
    # plt.axis([0, 16, 0, 15])
    plt.show()

def absorb(lossel, proc):
    abs=0
    for xx in range(255):
        abs+=data_1[xx]*1.5**2*x*10/255
    print(abs)
    absEl=0
    absnon=0
    NstopX=0
    for xx in range(255):
        if absEl<=abs*proc:
            absEl += lossel[xx]
            absnon += data_1[xx] * 1.5 ** 2 * x * 10 / 255
            NstopX=xx
    return [abs*proc, absEl, NstopX, absnon]

def third_calc(Ek, I, proc):
    carrage = ion_loss_thic(Ek, I)
    powerabs=absorb(carrage[0], proc)
    xmap=np.linspace(0, x, 255)
    print(f'Толщина фильтра {round(xmap[powerabs[2]]*10, 3)} мм Поглощение фотонов {round(powerabs[3], 3)} Вт Поглощение электронов {round(powerabs[1], 3)} Вт')

    plt.plot(np.linspace(0, x * 10, 255), carrage[1], label=f'Поток электронов I={I * 1.e3} мА E={Ek * 1.e-6} МэВ')
    plt.plot(np.linspace(0, x * 10, 255), data_1, label='Поток фотонов')
    plt.axvline(x=xmap[powerabs[2]]*10)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Длина пробега, мм', fontsize=16)
    plt.ylabel('Плотность поглощаемой мощности, Вт/мм³', fontsize=16)
    # plt.title(f'')
    plt.legend(fontsize=14)
    # plt.axis([0, xmap[powerabs[2]]*10, 0, 15])
    plt.show()

first_calc()
# second_calc(1.5e6, 16e-3)
# third_calc(1.5e6, 9e-3, 1)



