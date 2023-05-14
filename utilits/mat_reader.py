import numpy as np
import cmath
import plotly.graph_objects as go
import plotly.express as px
import math
import pandas as pd
import scipy.io
import matplotlib.pyplot as plt

filename = 'C:\\Users\\synchrotron\\Desktop\\NSU-station\\9kev\\frontend_aperture_total.mat'
data = scipy.io.loadmat(filename)
heat2D=data['total2D']

heat=sum(heat2D)

X=data['xbinEdges']
Y=data['ybinEdges']
x=X[0]
y=Y[0]
plt.subplot(223)
plt.imshow(data['total2D'])

plt.subplot(224)
plt.imshow(data['etotal1D_RGB'])

plt.colorbar()
plt.show()

true_power=data['power'][0][0]
print(data)