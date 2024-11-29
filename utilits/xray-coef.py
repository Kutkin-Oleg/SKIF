import numpy as np
import matplotlib.pyplot as plt

from xraydb import material_mu
from xraydb import atomic_density
energy = np.linspace(1000, 60000, 201)

muC = material_mu('C', energy)
muTi = material_mu('Ti', energy)
muAl = material_mu('Al', energy)
# mu is returned in 1/cm
transC = np.exp(-0.1 * muC)
transTi = np.exp(-0.1 * muTi)
transAl = np.exp(-0.1 * muAl)
fig = plt.figure(figsize=(10, 5))
plt.plot(energy, muC/10.e3, label='C, 2.267 г/см³')
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
# plt.plot(energy, muAl, label='Al, 2.7 г/см³')
# plt.plot(energy, muTi, label='Ti, 4.506 г/см³')

# plt.plot(energy, 1-trans, label='attenuated')
# plt.title('X-ray absorption by 1 mm of water')
# plt.yscale('log')
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Энергия (эВ)', fontsize=28)
plt.text(320, 16, 'К край', fontsize=16)
plt.ylabel('Линейный показатель \nпоглощения k, 1/мм', fontsize=28)
plt.legend(fontsize=14)
plt.show()

fig = plt.figure(figsize=(10, 5))
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.plot(energy, 1-transC, label='C, 2.267 г/см³')
plt.plot(energy, 1-transAl, label='Al, 2.7 г/см³')
plt.plot(energy, 1-transTi, label='Ti, 4.506 г/см³')


# plt.plot(energy, 1-trans, label='attenuated')
# plt.title('X-ray absorption by 1 mm of water')
# plt.yscale('log')
plt.xlabel('Энергия (эВ)', fontsize=28)
plt.ylabel('Коэффициент \nпоглощения', fontsize=28)
plt.legend(fontsize=14)
plt.show()


print(atomic_density('Al'))