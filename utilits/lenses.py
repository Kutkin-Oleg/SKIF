import xraydb
import numpy as np
import scipy.constants as constant

material='Al'
density=2.7
energy=16000
focus=2
R=0.2e-3
roughness=1.e-6
R0=1e-3
d=30.e-6

temp=[]
len=constant.h*constant.c/(energy/1.602e-19)
temp=xraydb.xray_delta_beta(material, density, energy)
mu=temp[1]*4*np.pi/len
k=2*np.pi/len
N=R/(2*temp[0]*focus)
Q=k*temp[0]
a=mu*N*R+2*N*Q**2*roughness**2
ap=a*R0**2/(2*R**2)
ap=mu*N*R0*2/(2*R)
Deff=2*R0*((1-np.exp(-ap))/ap)**0.5
w=R0**2/(2*R)
print(f'Декримент показателя преломления {material} равен {temp[0]}')
print(f'При фокусе {focus} м. требется {N} Линз')
print(f'Эффективная аппертура {Deff*1000} мм при радиусе кривизны {R*1000} мм')
print(f'Толщина линзы {(2*w+d)*1000} мм.\n')

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
Deff=2*R0*((1-np.exp(-ap))/ap)**0.5
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