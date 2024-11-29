import numpy as np
import matplotlib.pyplot as plt
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm
import pandas as pd
import plotly.graph_objs as go
import xrt.backends.raycing.materials_compounds as xcomp


def map_period_beta(E, theta,  mTop, mBot, mSub, name): # eV, degree
    refl_rs=[]
    beta=np.linspace(0.1,0.9,100)
    period=np.linspace(30, 35, 1000)
    for tempbeta in beta:
        tempr=[]
        for tempperiod in period:
            mL = rm.Multilayer(mTop, tempperiod*tempbeta, mBot, tempperiod*(1-tempbeta), 300, mSub)
            rs, rp = mL.get_amplitude(E, np.sin(np.deg2rad(theta)))
            tempr.append(abs(rs)**2)
        refl_rs.append(tempr)

    df = pd.DataFrame(data=refl_rs, columns=period,  index=beta)
    print(df)
    c=df.max()
    c=c.transpose()
    print(f'оптимальный период {round(c.idxmax(),3)}')
    c=df
    c=c.transpose()
    c=c.max()
    c=c.transpose()
    print(f'оптимальный beta {round(c.idxmax(),3)}')
    print(f'оптимальный R {round(c.max(),3)}')


    fig = go.Figure(data=go.Heatmap(colorbar={"title": "R"},
                                        z=df, x=period, y=beta))
    fig.update_layout(title_text=f'{name} при энергии {E} эВ и угле {round(theta, 3)} °',xaxis_title='d, ангстрем',yaxis_title='beta',font=dict(size=30))
    # fig.write_image(f"C:\\Users\\Oleg\\Desktop\\ВКР\\картинки\\0,5стеклоуглерод.png")
    fig.show()
    return 0




def relf2angle( E, d, beta, mTop, mBot, mSub, name):
    mL = rm.Multilayer(mTop, beta*d, mBot, (1-beta)*d, 300, mSub)
    theta = np.linspace(1, 10, 1001)  # degrees
    rs, rp = mL.get_amplitude(E, np.sin(np.deg2rad(theta)))[0:2]

    plt.plot(theta, abs(rs)**2, theta, abs(rp)**2)
    plt.title(f' Зависимость отражения {name}  d={d/10} нм и β={beta} от угла при энергии {E} эВ')
    plt.grid()
    plt.ylabel(r'R')
    plt.xlabel(r'угол, °')
    # plt.yscale('log')
    plt.show()
    return 0

def relf2angle( E, d, beta, mTop, mBot, mSub, name):
    mL = rm.Multilayer(mTop, beta*d, mBot, (1-beta)*d, 300, mSub)
    theta = np.linspace(1, 90, 1001)  # degrees
    rs, rp = mL.get_amplitude(E, np.sin(np.deg2rad(theta)))[0:2]

    plt.plot(theta, abs(rs)**2, theta, abs(rp)**2)
    plt.title(f' Зависимость отражения {name}  d={round(d/10,3)} нм и β={beta} от угла при энергии {E} эВ')
    plt.grid()
    plt.ylabel(r'R')
    plt.xlabel(r'угол, °')
    # plt.yscale('log')
    plt.show()
    return 0

def relf2energy( theta, d, beta, mTop, mBot, mSub, name, show=True):
    mL = rm.Multilayer(mTop, beta*d, mBot, (1-beta)*d, 300, mSub)
    E= np.linspace(100, 3000, 1001)  # degrees
    # print(E)
    rs, rp = mL.get_amplitude(E, np.sin(np.deg2rad(theta)))[0:2]
    # print(abs(rs)**2)
    if show:
        plt.plot(E, abs(rs)**2, E, abs(rp)**2)
        plt.title(f' Зависимость отражения {name}  d={round(d/10,3)} нм и β={beta} от энергии при угле {round(theta, 3)} °')
        plt.grid()
        plt.ylabel(r'R')
        plt.xlabel(r'Энергия, эВ')
        plt.yscale('log')
        plt.show()
    return abs(rs)**2


def main():
    name=f'W/B4C'
    mTop = rm.Material('W', rho=19.254)
    mBot = xcomp.BoronCarbide()
    mSub = rm.Material('Si', rho=2.32)
    # map_period_beta(2472, np.rad2deg(50.e-3))
    # relf2angle(2472, 53.2, 0.4)
    # relf2energy(np.rad2deg(50.e-3), 53.2, 0.4)

    name=f'W/SiC'
    mTop = rm.Material('W', rho=19.254)
    mBot = xcomp.SiliconCarbide()
    mSub = rm.Material('Si', rho=2.32)
    # map_period_beta(2472, np.rad2deg(50.e-3))
    # relf2angle(2472, 53.3, 0.4)
    # relf2energy(np.rad2deg(50.e-3), 53.3, 0.4)

    name=f'Cr/C'
    mTop = rm.Material('Cr', rho=2.99)
    mBot = rm.Material('C', rho=2.266)
    mSub = rm.Material('Si', rho=2.32)
    # map_period_beta(2472, np.rad2deg(50.e-3))
    # relf2angle(2472, 51.9, 0.4)
    # relf2energy(np.rad2deg(50.e-3), 51.9, 0.4)

    name=f'Ru/C'
    mTop = rm.Material('Ru', rho=12.41)
    mBot = rm.Material('C', rho=2.266)
    mSub = rm.Material('Si', rho=2.32)
    # map_period_beta(2472, np.rad2deg(50.e-3))
    # relf2angle(2472, 53.5, 0.5)
    # relf2energy(np.rad2deg(50.e-3), 53.5, 0.5)

    name=f'Mo/B4C'
    mTop = rm.Material('Mo', rho=10.22)
    mBot = xcomp.BoronCarbide()
    mSub = rm.Material('Si', rho=2.32)
    # map_period_beta(2472, np.rad2deg(50.e-3))
    # relf2angle(2472, 52.5, 0.4)
    # relf2energy(np.rad2deg(50.e-3), 52.5, 0.4)

    name = f'Fe/C'
    mTop = rm.Material('Fe', rho=7.874)
    mBot = rm.Material('C', rho=2.266)
    mSub = rm.Material('Si', rho=2.32)
    # map_period_beta(409.9, 87, mTop, mBot, mSub, name)
    # relf2angle(284.2, 43.8, 0.3)
    # relf2energy(87, 43.8, 0.3)

    name=f'Cr/Sc'
    mTop = rm.Material('Sc', rho=7.192)
    mBot = rm.Material('Cr', rho=2.99)
    mSub = rm.Material('Si', rho=2.32)
    map_period_beta(409.9, 87, mTop, mBot, mSub, name)
    # relf2angle(284.2, 43.8, 0.3)
    # relf2energy(87, 43.8, 0.3)

if __name__ == '__main__':
    main()

