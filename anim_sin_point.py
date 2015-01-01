#!/usr/bin/env python
from __future__ import division
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation


## Physical Constants ################################
l = 1             ## (m) spatial wavelength
k = 2*np.pi / l     ## (m^-1) wave number
dx = l/4            ## (m) actuator spacing

T = 2               ## (s) temporal period
w = -2 * np.pi / T   ## (s^-1) angular frequency

c = w/k             ## (m/s) wave speed

dt = 0.1            ## (s) time step interval
A = .05             ## (m) wave amplitude
off = 0.2           ## (m) wave offset

N = 2   ## number of actuators
S = 1   ## skip actuators

## Data ##############################################
## actuator x position
X = np.arange(0, dx*N, dx*S)
X2 = np.arange(0, dx * (N - 1 + S/8) , dx*S/8)

## actuator y position
def Y(x, i):
    """ continuous actuator """
    return off + A * np.sin(k*x - w*dt*i)


def Y2(x, i):
    """ binary (open-closed) actuator """
    out = np.sin(k*x-w*dt*i)
    out[out>=0] = 1
    out[out<0] = -1
    out *= A
    return out + off


def update_plot(i, l1, l2, l3, l4, tobj):
    l1.set_data(np.array([X, Y2(X, i)]))
    l2.set_data(np.array([X2, Y(X2, i)]))
    l3.set_data(np.array([X, -Y2(X, i) ]))
    l4.set_data(np.array([X2, -Y(X2, i)]))
    tobj.set_text("t=%2.1f" % (i*dt))
    return l1,l2,l3,l4,tobj

if __name__ == "__main__":
    fig1 = plt.figure()

    l4, = plt.plot([], [], 'bo-')
    l3, = plt.plot([], [], 'ro-')
    l2, = plt.plot([], [], 'bo-')
    l1, = plt.plot([], [], 'ro-')

    tobj = plt.text(-0.1,0,"")

    plt.xlim(-.5, .5)
    plt.ylim(-1, 1)
    plt.xlabel('position, $X$')
    plt.ylabel('actuator height, $Y$')
    plt.title(r'$Y=A\ \sin(k x - w t)$' + '\n$k=$' +
              '%2.3f' % k + ' $m^{-1}$   $w=$'+
              '%2.3f' % w + ' $s^{-1}$')

    ## FuncAnimation(figure, update_func, number of iterations, updater_args,
    ##              time delay between spacing, update new data only)
    line_ani = animation.FuncAnimation(fig1, update_plot, int(T/dt), fargs=(l1, l2, l3, l4, tobj),
        interval=dt*1000, blit=False)

    #line_ani.save('lines.mp4')

    print "plotting"
    plt.show()