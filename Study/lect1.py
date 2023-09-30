l1=[2,4,3,5,3,2,7,6,4,13,10]
temp=[]
for ii in range(len(l1)):
    if (ii<=1) or (ii>=5):
        temp.append(l1[ii])
l1=temp
print(l1)
for ii in range(len(l1)):
    if l1[ii]>5:
        print(l1[ii])
l1=[2,3,4]
l2=[5,7,8]
for ii in range(len(l2)):
    l1.append(l2[ii])
print(l1)
l1=[2,4,3,5, 3,2,7,6,4,13,10]
temp=[]
for ii in range(len(l1)):
    if (ii!=1) and (ii!=3) and (ii!=7):
        temp.append(l1[ii])
l1=temp
print(l1)
l1=[2,4,3,5,3,2,7,6,4,13,10]
temp=[]
for ii in range(len(l1)):
    if ii%2==0:
        temp.append(l1[ii])
l1=temp
print(l1)
l1=[2,3,4]
l2=[7,3,2]
for ii in range(len(l1)):
    l1[ii]=l1[ii]+l2[ii]
print(l1)
l1=[2,4,1,3,5,1,1,3,2,7,6,4,1,13,1,10]
for ii in range(len(l1)):
    if l1[ii]==1:
        print(ii)
        break
l1=[2,4,3,5,3,2,7,6,4,13,10]
cmax=0
cmin=0
for i in l1:
    if i==min(l1):
        cmin+=1
    if i==max(l1):
        cmax+=1
l2=[min(l1), max(l1), cmin, cmax]
print(l2)
l1=[13,40,16,11,15,40,13,16,11,16,16,13,11]
temp=0
dict0=dict()
for ii in l1:
    temp=0
    for xx in l1:
        if xx==ii:
            temp+=1
    dict0[ii]=temp
print(dict0)
dd1 = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g'}
dd2=dict()
temp=dd1.setdefault(2)
for ii in range(len(dd1)):
    dd2[ii+1]=dd1.setdefault(ii+1)
print(dd2)
