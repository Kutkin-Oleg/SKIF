import xraydb
import numpy as np
import scipy.constants as constant
import scipy.special as special


material='Be'
# density gr/sm^3
density=1.848
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
mu=0.507*100
# mu=temp[1]*4*np.pi/len
# mu=temp[2]*100

N=round(R/(2*temp[0]*focus))
w=R0**2/(2*R)
ap=mu*N*w
Deff1=2*R0*((1-np.exp(-ap))/ap)**0.5


Q0=k*temp[0]
ap=mu*R0**2/(focus*temp[0])/4
ap=-0.5*mu/(density*1000)*(np.pi*R0**2/focus)*(xraydb.atomic_mass(material)*1.66e-27/(6.02e23*2.82e-15*xraydb.f1_chantler(material, energy)*len**2*1.602e-19))
print(xraydb.f1_chantler(material, energy))
transmit=np.exp(-mu*N*d)*(1/(2*ap))*(1-np.exp(-2*ap))


a=mu*N*R+2*N*Q0**2*roughness**2
ap=a*R0**2/(2*R**2)
Deff2=2*R0*((1-np.exp(-ap))/ap)**0.5
Q=N**0.5*k*temp[0]
damping=np.exp(-Q**2*roughness**2)

v=temp[1]/temp[0]
Deff3=(len*focus/(2*v))**0.5*special.erf((2*np.pi*v/(len*focus))**0.5*R0)

Tc=R*np.exp(-mu*N*(R0**2/R+d))/(2*mu*N*R0**2)

Deff4=(2*R/(mu*N))**0.5
print(f'Декримент показателя преломления {material} равен {round(temp[0],9)}')
print(f'При фокусе {focus} м. требуется {N} Линз')
print(f'Эффективная апертура Lengeler {round(Deff1*1000,3)} мм при радиусе кривизны {R*1000} мм')
print(f'Эффективная апертура Lengeler с шероховатостью {round(Deff2*1000,3)} мм при радиусе кривизны {R*1000} мм')
print(f'Эффективная апертура Kohn {round(Deff3*1000,3)} мм при радиусе кривизны {R*1000} мм')
print(f'Толщина линзы {round(N*(2*w+d)*1000,3)} мм.')
print(f'Затухание интенсивности  {round(damping,3)}')
print(f'Коэффициент пропускания T  {round(transmit*100,3)} %')
print(f'Коэффициент пропускания Tc  {round(Tc*100,3)} %')
print(f'momentum transfer Q  {round(Q)}\n')

