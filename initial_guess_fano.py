# -*- coding: utf-8 -*-
"""
@author: dericsession
"""

import matplotlib.pyplot as plt
import numpy as np
from lmfit import Model

#insert file name below
data = np.loadtxt('Bsweep_B=pm9T@0p1T_32p4-32p65MHz_down')

BV=data[:,0]
f=data[:,1]
S21=data[:,2]


#lower and upper frequency limits
lf=32.4
hf=32.65
#function for our Lorentzian fit
def Fano(f,F0,q,r,A):
    L0=f-F0+q*r/2
    L1=(r/2)**2+(f-F0)**2  
    
    return A*L0**2/L1

#uses lmfit to change the function to a model
Lmodel = Model(Fano)

a=0
b=0
for a in range(len(BV)):
    if BV[a]==0: #this voltage value can be any that is in the range 
                   #of the data, I recommend using the lowest value
    
        if f[a]>=lf and f[a]<=hf:
            b+=1
#b gives the number of frequencies measured for each gate voltage
S21n=np.zeros(b)
fn=np.zeros(b)

i=0
j=0
    
for i in range(len(BV)):
        if BV[i]==0: #this is the B field that you are doing the fit at
            if f[i]>=lf and f[i]<=hf:
                fn[j]=f[i]
                S21n[j]=10**(S21[i]/20)
                j+=1
'''
#initial guess forward
fA0=-61.4609102
fB0=0.18631428
fH0=0.04821539
ff00=25.3
fG0=0.03543486
fphi0=1
'''

#initial guess backward
 #for 9.5V 
F00=32.5709819
q0=-3
r0=0.00230059
A0=20
#contraints if you need them. I usually use the first one to get the fit in
#the observable range of f0.
#Lmodel.set_param_hint('f0',min=18.8,max=23.5)
#Lmodel.set_param_hint('phi',min=-4,max=4)

result = Lmodel.fit(S21n,f=fn,F0=F00,q=q0,r=r0,A=A0)

          
print(result.fit_report())



plt.plot(fn,S21n,'bo')
#plt.plot(fn,result.init_fit,'k--')
plt.plot(fn,result.best_fit,'r-')
plt.xlabel('f (MHz)',fontsize=20)
plt.ylabel('$S_{21}$ (10^dB/20)',fontsize=20)
plt.xticks(fontsize=15)
plt.yticks([10**-62/20,10**(-58/20),10**(-54/20),10**(-50/20),10**(-46/20)],fontsize=15)
#plt.title('Resonator 22 a_D2cz1 at Vg = -20 V',fontsize=30)
plt.show()
