import xraydb
import numpy as np
import scipy.constants as constant
import scipy.special as special

material='Be'
density=1.848
energy=17000
focus=0.4239
R=50e-6
roughness=1.e-6
R0=632.5e-6/2
d=30.e-6

temp=[]
len=constant.h*constant.c/(energy*1.602e-19)
temp=xraydb.xray_delta_beta(material, density, energy)
mu=xraydb.material_mu(material, energy, density=None, kind='total')
mu=temp[1]*4*np.pi/len
k=2*np.pi/len
N=R/(2*temp[0]*focus)
w=R0**2/(2*R)
ap=mu*N*w
Deff1=2*R0*((1-np.exp(-ap))/ap)**0.5
Q=N**0.5*k*temp[0]
damping=np.exp(-Q**2*roughness**2)
transmit=1/(2*ap)*(1-np.exp(-2*ap))
v=temp[1]/temp[0]
Deff2=(len*focus/(2*v))**0.5*special.erf((2*np.pi*v/(len*focus))**0.5*R0)

print(f'Декримент показателя преломления {material} равен {temp[0]}')
print(f'При фокусе {focus} м. требуется {N} Линз')
print(f'Эффективная апертура Lengeler {Deff1*1000} мм при радиусе кривизны {R*1000} мм')
print(f'Эффективная апертура Kohn {Deff2*1000} мм при радиусе кривизны {R*1000} мм')
print(f'Толщина линзы {(2*w+d)*1000} мм.')
print(f'Затухание интенсивности  {damping}')
print(f'Коэффициент пропускания T  {transmit}')
print(f'momentum transfer Q  {Q}\n')

material='C5O2H8'
temp=[]
len=constant.h*constant.c/(energy*1.602e-19)
temp=xraydb.xray_delta_beta(material, density, energy)
mu=temp[1]*4*np.pi/len
k=2*np.pi/len
N=R/(2*temp[0]*focus)
Q=k*temp[0]
a=mu*N*R+2*N*Q**2*roughness**2
ap=a*R0**2/(2*R**2)
# Deff=2*R0*((1-np.exp(-ap))/ap)**0.5
Deff=(len*focus*temp[0]/temp[1])**0.5*special.erf((np.pi*temp[1]/(temp[0]*len*focus))**0.5*R0)
w=R0**2/(2*R)
print(f'Декримент показателя преломления {material} равен {temp[0]}')
print(f'При фокусе {focus} м. требется {N} Линз')
print(f'Эффективная аппертура {Deff*1000} мм при радиусе кривизны {R*1000} мм')
print(f'Толщина линзы {(2*w+d)*1000} мм.\n')




material='C2H4'
density=0.925
temp=[]
temp=xraydb.xray_delta_beta(material, density, energy)
mu=temp[1]*4*np.pi/len
k=2*np.pi/len
N=R/(2*temp[0]*focus)
Q=k*temp[0]
a=mu*N*R+2*N*(Q**2)*roughness**2
ap=a*R0**2/(2*R**2)
Deff=2*R0*((1-np.exp(-ap))/ap)**0.5
print(f'Декримент показателя преломления {material} равен {temp[0]}')
print(f'При фокусе {focus} м. требется {N} Линз')
print(f'Эффективная аппертура {Deff*1000} мм при радиусе кривизны {R*1000} мм')
print(f'Толщина линзы {(2*w+d)*1000} мм.\n')