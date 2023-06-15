import xraydb

material='C14H18O7'
density=1.2
energy=8200
temp=[]
temp=xraydb.xray_delta_beta(material, density, energy)
print(temp[0])
material='C2H4'
density=0.925
energy=17000
temp=[]
temp=xraydb.xray_delta_beta(material, density, energy)
print(temp[0])