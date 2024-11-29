import matplotlib.pyplot as plt
import numpy as np
import xraydb

# high absorbtion material
material_high='C'
# high material density
density_high=1.9
# low absorbtion material
material_low='V'
# low material density
density_low=6.11
# substrate material
material_s='SiO2'
# low material density
density_s=2.8

# target energy
energy=394.8
# angle from normal grad
angle=3

fi0=angle*np.pi/180


lightspeed=3.e8
wavelengh=(6.6e-34*lightspeed)/(energy*1.6e-19)
wavelengh=6.02e-9
# print(wavelengh)


n_high = xraydb.xray_delta_beta(material_high, density_high, energy)
eps1=((complex(1-n_high[0], -n_high[1]))**2)/(1+1.e-4)

n_low = xraydb.xray_delta_beta(material_low, density_low, energy)
eps2=((complex(1-n_low[0], -n_low[1]))**2)/(1+1.e-4)
print(n_high)
print(n_low)
print(eps1)
print(eps2)
n_s = xraydb.xray_delta_beta(material_s, density_s, energy)
epss=((complex(1-n_s[0], -n_s[1]))**2)/(1+1.e-4)

def reflectivity_brag(fi, d, N):
    # order of reflection
    n=1
    beta=0.3

    # sigma=1 for s polarization, sin(2*fi) for p polarization
    # sigma=np.sin(2*fi)
    sigma=1
    # average on the period eps
    mu = beta * eps1 + (1 - beta) * eps2
    # print(mu)
    L = N * d

    Bn=2*(eps1-eps2)*np.sin(np.pi*n*beta)/(np.pi*n)
    bn=(n*wavelengh/(2*d))**2+(np.sin(fi))**2-mu

    print(abs(mu))
    print(abs(Bn))
    print(abs(bn))
    Sn=(np.pi*n/(2*d*np.cos(fi)**2)*(Bn**2*sigma**2/4-bn**2)**0.5)

    R=(abs(Bn*sigma/2*np.tanh(Sn*L)/(bn*np.tanh(Sn*L)-(-1)**0.5*(Bn**2*sigma**2/4-bn**2)**0.5)))**2
    # half inf mirror
    # R=(abs(Bn*sigma/2/(bn-(-1)**0.5*(Bn**2*sigma**2/4-bn**2)**0.5)))**2
    # print(abs(R))
    return ((R))

def reflectivity(fi, d, N):
    # order of reflection
    n=1
    beta=0.3
    l1=beta*d
    l2=(1-beta)*d

    # sigma=1 for s polarization, sin(2*fi) for p polarization
    # sigma=np.sin(2*fi)
    sigma=1

    ksi1=2*np.pi/wavelengh*(eps1-np.sin(fi)**2)**0.5
    ksi2 = 2 * np.pi / wavelengh * (eps2 - np.sin(fi) ** 2) ** 0.5
    psi1=ksi1*l1
    psi2=ksi2*l2
    psi=psi1+psi2
    r=(eps1-eps2)*sigma/(4*np.cos(fi)**2)
    # print(abs(r)**2)
    ksi=(np.cos(psi)-r**2*np.cos(psi1-psi2))/(1-r**2)
    R=abs((2*(-1)**2*r*np.exp((-1)**0.5*psi2)*np.sin(psi1)*np.sin(N*np.arccos(ksi)))/(np.exp((-1)**0.5*(1-r**2*np.exp(2*(-1)**0.5*psi1)*np.sin(N*np.arccos(ksi))-(1-r**2)*np.sin((N-1)*np.arccos(ksi))))))**2
    return (R)

def reflectivity_Kohn(theta, d, N, beta):
    ksi1 = (eps1 - 1)
    ksi2 = (eps2 - 1)
    ksis = (epss - 1)
    kz1 = 2 * np.pi / wavelengh * ((np.sin(theta)) ** 2 + ksi1)**0.5
    kz2 = 2 * np.pi / wavelengh * ((np.sin(theta)) ** 2 + ksi2)**0.5
    kzs = 2 * np.pi / wavelengh * ((np.sin(theta)) ** 2 + ksis)**0.5

    C1 = np.exp((-1) ** 2 * kz1 * d * beta / 2)
    C2 = np.exp((-1) ** 2 * kz2 * d * (1-beta) / 2)

    r0 = (kz1 - kzs) / (kz1 + kzs) * C1 ** 2
    r  = (kz2 - kz1) / (kz1 + kz2) * C2 ** 2
    r_ = (kz1 - kz2) / (kz1 + kz2) * C1 ** 2
    t  = 2 * kz2 / (kz2 + kz2) * C1 * C2
    t_ = 2 * kz1 / (kz1 + kz2) * C1 * C2

    psi=2*np.arccos((1+t*t_-r*r_)/(2*(t*t_)**0.5))
    fi=np.log(-t*t_*(-1)**0.5)
    fpl = 1 - np.exp((-1) ** 0.5 * (fi + psi) / 2)
    fmn = 1 - np.exp((-1) ** 0.5 * (fi - psi) / 2)

    Rn = r * (r - r0 * fmn - ( r - r0 * fpl) * np.exp((-1) ** 0.5 * N * psi)) / (fpl * (r - r0 * fmn) - fmn * (r -r0 * fpl) * np.exp((-1) ** 0.5 * N* psi))
    # Rn=r*(1-np.exp((-1)**0.5*N*fi))/(1-np.exp((-1)**0.5*fi))+r0*np.exp((-1)*N*fi)

    print(f'{theta/np.pi*180} {ksi1}')
    return (abs(Rn.real))


def main():
    # Refl_arr=[]
    # period_arr=np.linspace(1e-10, 50e-9,1000)
    # for period in period_arr:
    #     Refl_arr.append(reflectivity(18*np.pi/180, period, 200))
    #
    # plt.plot( period_arr, Refl_arr)
    # plt.ylabel(r'R')
    # plt.xlabel(r'd, нм')
    # plt.title(f' Зависимость отражения от периода при угле {angle}°')
    #
    # plt.yscale('log')
    # plt.grid(True)
    # plt.show()

    # Refl_arr=[]
    # angle_arr=np.linspace(0, 80,10000)
    # for fix in angle_arr:
    #     # Refl_arr.append(reflectivity_Kohn(fix, 3.85e-9, 100, 0.5))
    #     # Refl_arr.append(reflectivity_brag(fix*np.pi/180 , 0.32e-9, 200))
    #     Refl_arr.append(reflectivity(fix * np.pi / 180, 0.32e-9, 200))
    # plt.plot( angle_arr, Refl_arr)
    # plt.ylabel(r'R')
    # plt.xlabel(r'град')
    # plt.title(f' Зависимость отражения от периода при угле {angle}°')
    #
    # plt.yscale('log')
    # plt.grid(True)
    # plt.show()

    formula = r'$R_N = \frac{r_{N-1, N} + r_{N, N+1}p_N^2}{1 + r_{N-1, N} r_{N, N+1} p_N^2}$'
    plt.text(0.01, 0.8, formula, fontsize=16)
    formula = r'$r_{j, j+1} = \frac{Q_j - Q_{j+1}}{Q_j + Q_{j+1}}$'
    plt.text(0.01, 0.4, formula, fontsize=16)
    formula = r'$r_{j, j+1} = \frac{Q_j - Q_{j+1}}{Q_j + Q_{j+1}}$'
    plt.text(0.01, 0.4, formula, fontsize=16)
    # Сохраняем как картинку
    plt.show()
    return 0

if __name__ == '__main__':
    main()



