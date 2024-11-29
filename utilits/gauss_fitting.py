import numpy as np
from scipy.optimize import curve_fit
import json
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from pylab import genfromtxt

path = 'C:\\Users\\Oleg\\Desktop\\ВКР\\spectra\\VEPP\\angle_pinhole_10keV-8.json'
with open(path) as f:
    spectra_source = json.load(f)

x=spectra_source["Output"]["data"][0]
y=spectra_source["Output"]["data"][1]
z=spectra_source["Output"]["data"][2]
qual=len(x)

with open('C:\\Users\\Oleg\\Desktop\\ВКР\\spectra\\VEPP_10keV.txt', 'w') as f:
    for i in range(qual):
        for j in range(qual):
            f.write(f'{x[i]} {y[j]} {z[i*255+j]}')
            f.write('\n')





x= np.asarray(x)
y = np.asarray(y)





def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

zslicex=[]
zslicey=[]
for i in range(qual):
    zslicex.append(z[i*round(qual)+round(qual/2)]/max(z))
    zslicey.append(z[round(qual/2)*round(qual)+i]/max(z))
z=np.asarray(z)
zslicex = np.asarray(zslicex)
zslicex = np.asarray(zslicey)

def oprox(obx, ord):
    mean = sum(obx*ord)/qual
    sigma = sum(ord*(obx - mean)**2)/qual
    popt, pcov = curve_fit(gauss_function, obx, ord, p0 = [1, mean, sigma])
    plt.plot(obx, gauss_function(obx, *popt), label='fit')
    plt.plot(obx, zslicex, label='x')
    plt.title(f'a={round(popt[0], 3)}, x0={round(popt[1], 3)}, sigma={round(popt[2], 3)}')
    print(f'a={round(popt[0], 6)}, x0={round(popt[1], 6)}, sigma={round(popt[2], 6)}')
    plt.legend()
    plt.show()
    return popt



def old():
    param1 = oprox(x, zslicex)
    param2 = oprox(x, zslicey)
    x, y = np.mgrid[x[0]:x[254]:255j, y[0]:y[254]:255j]
    # print(x)
    # Need an (N, 2) array of (x, y) pairs.
    xy = np.column_stack([x.flat, y.flat])

    mu = np.array([param1[1], param2[1]])

    sigma = np.array([param1[2], param2[2]])
    covariance = np.diag(sigma**2)

    znew = multivariate_normal.pdf(xy, mean=mu, cov=covariance)


    # Reshape back to a (30, 30) grid.
    znew = znew.reshape(x.shape)/max(znew)*param1[0]*param2[0]*1.e19

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x,y,znew)
    #ax.plot_wireframe(x,y,z)
    plt.show()

    z=z.reshape(x.shape)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x,y,-znew+z)
    #ax.plot_wireframe(x,y,z)

    plt.show()

def main():
    mat0 = genfromtxt('C:\\Users\\Oleg\\Desktop\\ВКР\\spectra\\VEPP_10keV.txt')

    def twoD_Gauss(xy, amplitude,x0,y0,sigma_x,sigma_y,offset):
        x0=float(x0)
        y0=float(y0)
        return offset + amplitude*np.exp(-(((xy[0]-x0)**(2)/(2*sigma_x**(2))) + ((xy[1]-y0)**(2)/(2*sigma_y**(2)))))

    x = mat0[:,0]
    y = mat0[:,1]
    z = mat0[:,2]

    data=mat0[:,2]

    # plot twoD_Gaussian data generated above
    ax = plt.axes(projection='3d')
    ax.plot_trisurf(x, y, data, cmap="jet", linewidth=0)

    #FITTING HELP!
    initial_guess = (1.e19,0,0,0.1,0.1,0)
    params, pcov = curve_fit(twoD_Gauss, [x, y], data,initial_guess)
    plt.show()
    print(f'амплитула {params[0]} x0={params[1]} y0={params[2]} sigmax={params[3]}, sigmay={params[4]}')
    ax = plt.axes(projection='3d')
    ax.plot_trisurf(x, y, twoD_Gauss([x,y], *params), cmap="jet", linewidth=0)
    plt.show()

if __name__ == '__main__':
    main()