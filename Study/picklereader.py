import pickle
data=[]
with open('C:/Users/Oleg/AppData/Local/Programs/Python/Python311/Lib/site-packages/xrt/lastRuns.pickle', 'wb') as f:
    pickle.load(f)
print(data)