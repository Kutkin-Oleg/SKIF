import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
from matplotlib.ticker import FixedFormatter
lenght=0.5*1.e-6
k=2*np.pi/lenght
ns=1.5
nf=2
nc=1.6


Nfi=500
N=3
fi_stack=np.linspace(0, np.pi/2, Nfi)
h=np.linspace(lenght/4, lenght*2, N)


rmte_stack=[[0] * Nfi for i in range(N)]
rphasete_stack=[[0] * Nfi for i in range(N)]
tmte_stack=[[0] * Nfi for i in range(N)]
tphasete_stack=[[0] * Nfi for i in range(N)]

rmte_stack_=[[0] * Nfi for i in range(N)]
rphasete_stack_=[[0] * Nfi for i in range(N)]
tmte_stack_=[[0] * Nfi for i in range(N)]
tphasete_stack_=[[0] * Nfi for i in range(N)]

rsf_stack= [0 for i in range(Nfi)]
rsf_stack_=[0 for i in range(Nfi)]
tsf_stack= [0 for i in range(Nfi)]
tsf_stack_=[0 for i in range(Nfi)]

for tempy in range(N):
    print(tempy)
    for tempx in range(Nfi):
        ksx=k*ns*np.cos(fi_stack[tempx])
        kfx = k * nf * np.cos(np.arcsin(np.sin(fi_stack[tempx])*ns/nf))
        kcx=k*nc*np.cos(np.arcsin(np.sin(fi_stack[tempx])*ns/nc))

        rsf=(ksx-kfx)/(ksx+kfx)
        rfc=(kfx-kcx)/(kfx+kcx)
        tsf=2*ksx/(ksx+kfx)
        tfc=2*kfx/(kfx+kcx)

        rsf_stack[tempx]=(abs(rsf))
        tsf_stack[tempx]=(abs(tsf))

        a1=rsf+rfc*np.cos(2*kfx*h[tempy])
        b1=rfc*np.sin(2*kfx*h[tempy])
        a2=1+rsf*rfc*np.cos(2*kfx*h[tempy])
        b2=rsf*rfc*np.sin(2*kfx*h[tempy])
        a3=tsf*tfc*np.cos(2*kfx*h[tempy])
        b3 = tsf * tfc * np.sin(2 * kfx * h[tempy])

        mte=(((a1*a2-+b1*b2)/(a2**2+b2**2))**2+((a1*b2-a2*b1)/(a2**2+b2**2))**2)**0.5

        # phase=np.arctan(rfc*np.sin(-2*kfx*h)/(rsf+rfc*np.cos(-2*kfx*h)))-np.arctan((rsf*rfc*np.sin(-2*kfx*h)/(1+rsf*rfc*np.cos(-2*kfx*h))))
        if (a1 * a2 + b1 * b2) > 0:
            phase=np.arctan((a1*b2-a2*b1)/(a1*a2+b1*b2))
        if ((a1 * a2 + b1 * b2) < 0) and (a1*b2-a2*b1>=0):
            phase=np.pi+np.arctan((a1*b2-a2*b1)/(a1*a2+b1*b2))
        if ((a1 * a2 + b1 * b2) < 0) and ((a1*b2-a2*b1)<0):
            phase=-np.pi+np.arctan((a1*b2-a2*b1)/(a1*a2+b1*b2))
        if ((a1 * a2 + b1 * b2) == 0) and ((a1*b2-a2*b1)>0):
            phase=np.pi/2
        if ((a1 * a2 + b1 * b2) == 0) and ((a1*b2-a2*b1)<0):
            phase=-np.pi/2


        rmte_stack[tempy][tempx]=(mte)
        rphasete_stack[tempy][tempx]=(phase)



        # tmte=(tsf*tfc)/((1+rsf*rfc*np.cos(2*kfx*h))**2+(-rsf*rfc*np.sin(2*kfx*h))**2)**0.5
        tmte=(((a3*a2+b3*b2)/(a2**2+b2**2))**2+((a3*b2-a2*b3)/(a2**2+b2**2))**2)**0.5
        # tphasete=np.pi/2-np.arctan((rsf*rfc*np.sin(-2*kfx*h)/(1+rsf*rfc*np.cos(-2*kfx*h))))
        if (a1 * a2 + b1 * b2) > 0:
            tphasete=np.arctan((a3*b2-a2*b3)/(a1*a2+b1*b2))
        if ((a1 * a2 + b1 * b2) < 0) and (a3*b2-a2*b3>=0):
            tphasete=np.pi+np.arctan((a3*b2-a2*b3)/(a1*a2+b1*b2))
        if ((a1 * a2 + b1 * b2) < 0) and ((a3*b2-a2*b3)<0):
            tphasete=-np.pi+np.arctan((a3*b2-a2*b3)/(a1*a2+b1*b2))
        if ((a1 * a2 + b1 * b2) == 0) and ((a3*b2-a2*b3)>0):
            tphasete=np.pi/2
        if ((a1 * a2 + b1 * b2) == 0) and ((a3*b2-a2*b3)<0):
            tphasete=-np.pi/2
        tmte_stack[tempy][tempx]=(tmte)
        tphasete_stack[tempy][tempx]=(tphasete)

        rsf_=((-ksx/ns**2)-(-kfx/nf**2))/((-ksx/ns**2)+(-kfx/nf**2))
        rfc_=((-kfx/nf**2)-(-kcx/nc**2))/((-kfx/nf**2)+(-kcx/nc**2))
        tsf_=2*(-ksx/ns**2)/((-ksx/ns**2)+(-kfx/nf**2))
        tfc_=2*(-kfx/nf**2)/((-kfx/nf**2)+(-kcx/nc**2))

        rsf_stack_[tempx]=(abs(rsf_))
        tsf_stack_[tempx]=(abs(tsf_))

        a1_ = rsf_ + rfc_ * np.cos(2 * kfx * h[tempy])
        b1_ = rfc_ * np.sin(2 * kfx * h[tempy])
        a2_ = 1 + rsf_ * rfc_ * np.cos(2 * kfx * h[tempy])
        b2_ = rsf_ * rfc_ * np.sin(2 * kfx * h[tempy])
        a3_ = tsf_ * tfc_ * np.cos(2 * kfx * h[tempy])
        b3_ = tsf_ * tfc_ * np.sin(2 * kfx * h[tempy])

        mte_ = (((a1_ * a2_ - +b1_ * b2_) / (a2_ ** 2 + b2_ ** 2)) ** 2 + ((a1_ * b2_ - a2_ * b1_) / (a2_ ** 2 + b2_ ** 2)) ** 2) ** 0.5

        # phase=np.arctan(rfc*np.sin(-2*kfx*h)/(rsf+rfc*np.cos(-2*kfx*h)))-np.arctan((rsf*rfc*np.sin(-2*kfx*h)/(1+rsf*rfc*np.cos(-2*kfx*h))))
        if (a1_ * a2_+ b1_ * b2_) > 0:
            phase_ = np.arctan((a1_ * b2_ - a2_ * b1_) / (a1_ * a2_ + b1_ * b2_))
        if ((a1_ * a2_ + b1_ * b2_) < 0) and (a1_ * b2_ - a2_ * b1_ >= 0):
            phase_ = np.pi + np.arctan((a1_ * b2_ - a2_ * b1_) / (a1_ * a2_ + b1_ * b2_))
        if ((a1_ * a2_ + b1_ * b2_) < 0) and ((a1_ * b2_ - a2_ * b1_) < 0):
            phase_ = -np.pi + np.arctan((a1_ * b2_ - a2_ * b1_) / (a1_ * a2_ + b1_ * b2_))
        if ((a1_ * a2_ + b1_ * b2_) == 0) and ((a1_ * b2_ - a2_ * b1_) > 0):
            phase_ = np.pi / 2
        if ((a1_ * a2_ + b1_ * b2_) == 0) and ((a1_ * b2_ - a2_ * b1_) < 0):
            phase_ = -np.pi / 2

        rmte_stack_[tempy][tempx]=mte_
        rphasete_stack_[tempy][tempx]=(phase_)

        tmte_ = (((a3_ * a2_ + b3_ * b2_) / (a2_ ** 2 + b2_ ** 2)) ** 2 + ((a3_ * b2_ - a2_ * b3_) / (a2_ ** 2 + b2_ ** 2)) ** 2) ** 0.5
        # tphasete=np.pi/2-np.arctan((rsf*rfc*np.sin(-2*kfx*h)/(1+rsf*rfc*np.cos(-2*kfx*h))))
        if (a1_ * a2_ + b1_ * b2_) > 0:
            tphasete_ = np.arctan((a3_ * b2_ - a2_ * b3_) / (a1_ * a2_ + b1_ * b2_))
        if ((a1_ * a2_ + b1_ * b2_) < 0) and (a3_ * b2_ - a2_ * b3_ >= 0):
            tphasete_ = np.pi + np.arctan((a3_ * b2_ - a2_ * b3_) / (a1_ * a2_ + b1_ * b2_))
        if ((a1_ * a2_ + b1_ * b2_) < 0) and ((a3_ * b2_ - a2_ * b3_) < 0):
            tphasete_ = -np.pi + np.arctan((a3_ * b2_ - a2_ * b3_) / (a1_ * a2_ + b1_ * b2_))
        if ((a1_ * a2_ + b1_ * b2_) == 0) and ((a3_ * b2_ - a2_ * b3_) > 0):
            tphasete_ = np.pi / 2
        if ((a1_ * a2_ + b1_ * b2_) == 0) and ((a3_ * b2_ - a2_ * b3_) < 0):
            tphasete_ = -np.pi / 2
        tmte_stack_[tempy][tempx]=(tmte_)
        tphasete_stack_[tempy][tempx]=(tphasete_)

for i in range(len(fi_stack)):
    fi_stack[i]=fi_stack[i]*180/np.pi

print(tmte_stack_[0])
def show_plot_mod( y1, y2):
    for temp in range(N):
        plt.plot(fi_stack, y1[temp], label=f'M(θs) h={h[temp]*1.e6} мкм')
    plt.plot(fi_stack, y2, 'r--', label='|rsf(θs)|')
    plt.xlabel("θ, град")
    plt.grid()
    # plt.ylabel("M(θs)")
    plt.legend()
    plt.show()
    return

def show_plot_phase(y1):
    fig = plt.figure()
    ax = fig.add_subplot()
    for temp in range(N):
        ax.plot(fi_stack, y1[temp], label=f'h={h[temp]*1.e6} мкм')
    plt.grid()
    plt.legend()
    plt.xlabel("θ, град")
    plt.ylabel("Ф(θs)")
    ax.yaxis.set_major_locator(FixedLocator([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi]))
    ax.yaxis.set_major_formatter(FixedFormatter(['-π', '-π/2', '0', 'π/2', 'π']))
    plt.show()
    return

def show_plot_modphase(y1,f):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax2 = ax1.twinx()
    line1=ax1.plot(fi_stack, y1, label='M(θs)')
    line2=ax2.plot(fi_stack, f,'r--', label='Ф(θs)', color='green')
    ax2.yaxis.set_major_locator(FixedLocator([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi]))
    ax2.yaxis.set_major_formatter(FixedFormatter(['-π', '-π/2', '0', 'π/2', 'π']))
    ax2.grid(True)
    ax1.set_xlabel("θ, град")
    ax1.grid()
    lns=line1+line2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs,  frameon=False)
    plt.show()
    return

show_plot_mod(rmte_stack, rsf_stack)
show_plot_phase(rphasete_stack)
show_plot_modphase(rmte_stack[2], rphasete_stack[2])

show_plot_mod(tmte_stack, tsf_stack)
show_plot_phase(tphasete_stack)
show_plot_modphase(tmte_stack[2], tphasete_stack[2])

show_plot_mod(rmte_stack_, rsf_stack_)
show_plot_phase(rphasete_stack_)
show_plot_modphase(rmte_stack_[2], rphasete_stack_[2])

show_plot_mod(tmte_stack_, tsf_stack_)
show_plot_phase(tphasete_stack_)
show_plot_modphase(tmte_stack_[2], tphasete_stack_[2])
# plt.plot(fi_stack, rmte_stack, label='M(θs)')
# plt.plot(fi_stack, rsf_stack, 'r--', label='|rsf(θs)|')
# plt.xlabel("θ, град")
# plt.grid()
# # plt.ylabel("M(θs)")
# plt.legend()
# plt.show()
#
# fig = plt.figure()
# ax = fig.add_subplot()
# ax.plot(fi_stack, rphasete_stack)
# plt.grid()
# plt.xlabel("θ, град")
# plt.ylabel("Ф(θs)")
# ax.yaxis.set_major_locator(FixedLocator([-np.pi, -np.pi/2,0, np.pi/2, np.pi]))
# ax.yaxis.set_major_formatter(FixedFormatter(['-π', '-π/2', '0', 'π/2', 'π']))
# plt.show()
#
# plt.plot(fi_stack, tmte_stack, label='M(θs)')
# plt.plot(fi_stack, tsf_stack, 'r--', label='|tsf(θs)|')
# plt.grid()
# plt.xlabel("θ, град")
# # plt.ylabel("M(θs)")
# plt.legend()
# plt.show()
#
# fig = plt.figure()
# ax = fig.add_subplot()
# ax.plot(fi_stack, tphasete_stack)
# plt.grid()
# plt.xlabel("θ, град")
# plt.ylabel("Ф(θs)")
# ax.yaxis.set_major_locator(FixedLocator([-np.pi, -np.pi/2,0, np.pi/2, np.pi]))
# ax.yaxis.set_major_formatter(FixedFormatter(['-π', '-π/2', '0', 'π/2', 'π']))
# plt.show()
#
# plt.plot(fi_stack, rmte_stack_, label='M(θs)')
# plt.plot(fi_stack, rsf_stack_, 'r--', label='|rsf(θs)|')
# plt.grid()
# plt.xlabel("θ, град")
# # plt.ylabel("M(θs)")
# plt.legend()
# plt.show()

# fig = plt.figure()
# ax = fig.add_subplot()
# ax.plot(fi_stack, rphasete_stack_)
# plt.grid()
# plt.xlabel("θ, град")
# plt.ylabel("Ф(θs)")
# ax.yaxis.set_major_locator(FixedLocator([-np.pi, -np.pi/2,0, np.pi/2, np.pi]))
# ax.yaxis.set_major_formatter(FixedFormatter(['-π', '-π/2', '0', 'π/2', 'π']))
# plt.show()
#
# plt.plot(fi_stack, tmte_stack_, label="M(θs)")
# plt.plot(fi_stack, tsf_stack_, 'r--', label='|tsf(θs)|')
# plt.grid()
# plt.xlabel("θ, град")
# # plt.ylabel("M(θs)")
# plt.legend()
# plt.show()
#
# fig = plt.figure()
# ax = fig.add_subplot()
# ax.plot(fi_stack, tphasete_stack_)
# plt.grid()
# plt.xlabel("θ, град")
# plt.ylabel("Ф(θs)")
# ax.yaxis.set_major_locator(FixedLocator([-np.pi, -np.pi/2,0, np.pi/2, np.pi]))
# ax.yaxis.set_major_formatter(FixedFormatter(['-π', '-π/2', '0', 'π/2', 'π']))
# plt.show()