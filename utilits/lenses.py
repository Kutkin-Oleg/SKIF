import xraydb
import numpy as np
import scipy.constants as constant
import scipy.special as special


material='C4H6O2'
# density gr/sm^3
density=0.962
# Energy of x-ray radiation eV
energy=17000
# Focus length of lenses m
focus=12
# radius of curvation m
R=0.5e-3
# roughness m
roughness=0.1e-6
# physical radius m
R0=1.393e-3/2
d=30.e-6

temp=[]
len=constant.h*constant.c/(energy*1.602e-19)
k=2*np.pi/len
# delta : real part of index of refraction beta : imag part of index of refraction atlen : attenuation length in cm
temp=xraydb.xray_delta_beta(material, density, energy)

# Attenuation coefficient 1/m
mu=xraydb.material_mu(material, energy, density=density, kind='total')*100
# mu Be
# mu=0.507*100
# mu Al
# mu=16.63*100
# mu Ni
# mu=492.757*100
print(mu)
N=round(R/(2*temp[0]*focus))
w=R0**2/(2*R)
ap=mu*N*w
Deff1=2*R0*((1-np.exp(-ap))/ap)**0.5


Q0=k*temp[0]
ap=mu*R0**2/(focus*temp[0])/4
ap=mu*R0**2*N/(2*R)
transmit=np.exp(-mu*N*d)*(1/(2*ap))*(1-np.exp(-2*ap))


a=mu*N*R+2*N*Q0**2*roughness**2
ap=a*R0**2/(2*R**2)
Deff2=2*R0*((1-np.exp(-ap))/ap)**0.5
Q=N**0.5*k*temp[0]
damping=np.exp(-Q**2*roughness**2)

v=temp[1]/temp[0]
Deff3=(len*focus/(2*v))**0.5*special.erf((2*np.pi*v/(len*focus))**0.5*R0)

Tplanar=(R*np.exp(-mu*N*(R0**2/R+d)))/(2*mu*N*R0**2)

Deff4=(2*R/(mu*N))**0.5

f0=R/(2*N*temp[0])
L=N*2*w
f=f0*(L/f0)**0.5/np.sin((L/f0)**0.5)
print(f'Декримент показателя преломления {material} равен {round(temp[0],9)}')
print(f'При задаваемом фокусе {focus} м. требуется {N} Линз')
print(f'Фокусное расстояние {round(f0,3)} м')
print(f'Фокусное расстояние в приближении толстой линзы {round(f,3)} м')
print(f'Эффективная апертура Lengeler {round(Deff1*1000,3)} мм при радиусе кривизны {R*1000} мм')
print(f'Эффективная апертура Lengeler с шероховатостью {round(Deff2*1000,3)} мм при радиусе кривизны {R*1000} мм')
print(f'Эффективная апертура Kohn {round(Deff3*1000,3)} мм при радиусе кривизны {R*1000} мм')
print(f'Толщина линзы {round(N*(2*w+d)*1000,3)} мм.')
print(f'Затухание интенсивности  {round(damping,3)}')
print(f'Коэффициент пропускания T  {round(transmit*100,3)} %')
print(f'Коэффициент пропускания T planar  {round(Tplanar*100,3)} %')
print(f'momentum transfer Q  {round(Q)}\n')


