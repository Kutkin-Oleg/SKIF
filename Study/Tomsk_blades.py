import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
ta = pd.read_table('C:\\Users\\Oleg\\Desktop\\конструкторам\\ta2.txt', sep='\s+', engine='python',  index_col=0)
# ta['Ta0,4мм']=ta['Ta0,4мм'].astype (float)
# ta['Ta0,45мм']=ta['Ta0,45мм'].astype (float)
# ta['Ta0,5мм']=ta['Ta0,5мм'].astype (float)
print(ta)
ta = ta.rename(columns={'9848.85': 'Ta 9,8кэВ','15430.4': 'Ta 15,4кэВ','20025.0': 'Ta 20кэВ','25028.0': 'Ta 25кэВ','30099.1': 'Ta 30,1кэВ','35000.0': 'Ta 35кэВ'})
# ta=ta.T
# ta.to_csv('C:\\Users\\Oleg\\Desktop\\ta2.txt')
ta.plot()
plt.grid()
plt.xlabel('Толщина ножа, мм')
plt.ylabel('I')
plt.legend(loc='best', fontsize=12)
plt.semilogy ()
plt.show()

