import numpy as np
from numpy import pi

import matplotlib as mpl
from matplotlib import pyplot as plt
plt.ion()
plt.rc('text', usetex=True)
plt.rc('font', family='serif',size=14)
#plt.rc('text.latex', preamble=r'\usepackage[T1]{fontenc}')
## Save size:
fig_w=8; fig_h=6; ## inches

deg=pi/180

### Constants ###
R=6370. #km
H=20.   #km,   needs calibration
l=12   #km,   needs calibration
UVI_0=55 #Normalization factor of UV index

lat =57.8*deg
tilt=23.5*deg

def d(theta):
    #theta is ange over horizon
    return R*(-np.sin(theta)+np.sqrt(np.sin(theta)**2+2*H/R+H**2/R**2))

def I(theta,l):
    return np.exp(-(d(theta))/l)

def Theta(t,T):
    # t: time of day in hours
    # T: time of year in days

    #offset=tilt*np.cos(2*pi*(T+10)/365)
    #if lat<-offset: offset=-offset
    #return (pi/2-lat)*np.cos(2*pi*t/24)-offset

    # Fomulas from http://www.jgiesen.de/astro/suncalc/calculations.htm
    y = (2*pi/365)*(T - 1 + (t-12)/24)
    declin = (0.006918-0.399912*np.cos(y)+0.070257*np.sin(y)-0.006758*np.cos(2*y)
              +0.000907*np.sin(2*y)-0.002697*np.cos(3*y)+0.00148*np.sin(3*y))
    
    return pi/2-np.arccos(np.sin(lat)*np.sin(declin)+np.cos(lat)*np.cos(declin)*np.cos(pi*t/12))




fig=plt.figure(num=1,figsize=(fig_w,fig_h))
fig.clf()
fig,ax1=plt.subplots(num=1,figsize=(fig_w,fig_h),nrows=1, ncols=1,sharex='col')
ax2=ax1.twinx()

t=np.linspace(-12,12,200,endpoint=True);






### User set time of year: (midsummer= 356/2-10)
T=365/2 -10 +10
#T=365/4 -10  +6


### plotting
#II=I(Theta(t,T),l)/I(((pi/2-57.8*deg)+tilt), l)
II=I(Theta(t,T),l)*UVI_0
#II*=3/II.max()

ax2.plot(t+12,Theta(t,T)/deg,'b')
ax2.set_ylim([0,90])
ax1.plot(t+12,II,'r')
ax1.set_ylim(bottom=0)
t_danger=t[np.where(II>2.5)]
if len(t_danger)>0:
    print("You should avoid the sun during solar noon +- %0.1f hours." % t_danger[-1])
else:
    print("Get some sun! It won't hurt.")




ax1.axvline(12,color='k',linestyle='--',linewidth=0.5)

# ax1.axvline(9,color='grey',linestyle=':',linewidth=0.5)
# ax1.axvline(15,color='grey',linestyle=':',linewidth=0.5)
# ax1.axhline(1,color='grey',linestyle=':',linewidth=0.5)

# ax1.axvline(10,color='grey',linestyle=':',linewidth=0.5)
# ax1.axhline(2,color='grey',linestyle=':',linewidth=0.5)


ax1.set_xlabel("Time of day (hour)")
ax2.set_ylabel("Solar angle above horizon (deg)",color='blue')
ax1.set_ylabel("UV index",color='red')

ax1.set_xlim([0,24])
ax1.set_xticks(range(25))
