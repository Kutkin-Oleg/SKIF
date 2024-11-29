import matplotlib.pyplot as plt
import numpy as np

# период ондулятора м
lamu=np.linspace(0.01,0.05,1000)
# ток катушки
I=1500
# расстоянние между магнитами
g=0.01

# коэффициенты поля на оси магнита

b=-3.65434
c=0.74528

# энергия первой гармоники
en=284.2


lightspeed=2.9979e8
lorenz=3.e9/(0.511e6)
e=1.602e-19
lamm=(6.6261e-34*lightspeed)/(en*e)
print(lamm)

me=9.109e-31
k1=[]
k2=[]

def diff_lamu():
    a = 0.00281 * I - 0.00336
    for x in lamu:
        B = a * np.exp(b *g/x+c*(g/x)**2)
        k1.append(e*x*B/(2*np.pi*me*lightspeed))
        k2.append((2*(lamm/x*2*lorenz**2-1))**0.5)

    plt.plot( lamu, k1, label='k1')
    plt.plot(lamu,k2,   label='k2')
    plt.ylabel(r'K')
    plt.xlabel(r'lamu, m')
    plt.title(r'')
    plt.legend(loc='best', fontsize=12)
    # plt.yscale('log')
    plt.grid(True)
    plt.show()

def diff_current(period, curarr):
    wave=[]
    Barr=[]
    karr=[]
    for x in curarr:
        a = 0.00281 * x - 0.00336
        B = a * np.exp(b *g/period+c*(g/period)**2)
        Barr.append(B)
        k=e*period*B/(2*np.pi*me*lightspeed)
        karr.append(k)
        wave.append(6.626e-34*lightspeed/(e*(period/(2*lorenz**2)*(1+k**2/2))))


    plt.plot( curarr, wave)
    plt.ylabel(r'Энергия 1й гармоники, эВ')
    plt.xlabel(r'ток, кА')
    plt.title(r'')
    # plt.yscale('log')
    plt.grid(True)
    plt.show()

    plt.plot(curarr, Barr)
    plt.xlabel(r'ток, кА')
    plt.ylabel(r'поле в центре, Тл')
    plt.title(r'')
    # plt.yscale('log')
    plt.grid(True)
    plt.show()

    plt.plot(Barr, wave)
    plt.ylabel(r'Энергия 1й гармоники, эВ')
    plt.xlabel(r'поле в центре, Тл')
    plt.title(r'')
    # plt.yscale('log')
    plt.grid(True)
    plt.show()

    plt.plot(karr, wave)
    plt.ylabel(r'Энергия 1й гармоники, эВ')
    plt.xlabel(r'K')
    plt.title(r'')
    # plt.yscale('log')
    plt.grid(True)
    plt.show()



diff_lamu()

cur=np.linspace(600,1500,100)
diff_current(0.035, cur)