'''
		EE2703 Applied Programming Lab - 2021
				Assignment-7: The Laplace Transform
	Name: SAKTHI HARISH D T
	Roll: EE19B054
'''
import scipy.signal as sgnl         #importing required libraries
import numpy as np
import matplotlib.pyplot as plt

gamma1= 0.5             #constants to be used in the program
gamma2= 0.05
w= 1.5

F_num= np.poly1d([1, gamma1])      #defining numerator of function with decay as 0.5 
FX_den= np.polymul([1, 2*gamma1, gamma1**2 + w**2], [1, 0, 2.25])      #defining denominator of X(s) after applying initial conditions 
X= sgnl.lti(F_num,FX_den)           
t,x= sgnl.impulse(X, None, np.linspace(0, 50, 1000))    #Getting the solution for x(t)

plt.figure(1)               #Plotting the solution for x(t) for 0.5 as decay
plt.plot(t, x, label='decay=0.5')
plt.xlabel(r"$t \to$")
plt.ylabel(r"$x(t) \to$")
plt.title(r'Solution of $\ddot{x} + 2.25x = e^{-0.5t}cos(1.5t)u(t)$')
plt.legend()
plt.grid()
plt.ylim(-1, 1)
plt.show()

F_num= np.poly1d([1, gamma2])        #defining numerator of function with decay as 0.05   
FX_den = np.polymul([1, 2*gamma2, gamma2**2 + w**2], [1, 0, 2.25])      #defining denominator of X(s) after applying I.C's
X= sgnl.lti(F_num,FX_den)
t,x= sgnl.impulse(X, None, np.linspace(0, 50, 1000))        #Getting the solution for x(t)

plt.figure(2)               #Plotting the solution for x(t) for 0.05 decay
plt.plot(t, x, label='decay=0.05')
plt.xlabel(r"$t \to$")
plt.ylabel(r"$x(t) \to$")
plt.title(r'Solution of $\ddot{x} + 2.25x = e^{-0.05t}cos(1.5t)u(t)$')
plt.legend()
plt.grid()
plt.show()

H1_s = sgnl.lti([1], [1, 0, 2.25])        # Transfer function H1(s)= X(s)/F(s)
plt.figure(3)                             #This block plots the response of the system for various frequencies
for w in np.arange(1.4, 1.6, 0.05):     
    T = np.linspace(0, 50, 1000)
    t, y, rest = sgnl.lsim(H1_s,U= np.exp(-0.05*t)*np.cos(w*t), T=T)
    plt.plot(t,y, label='$w = {} rad/s$'.format(w))
    plt.legend()
plt.xlabel(r"$t \to$")
plt.ylabel(r"$x(t) \to$")
plt.title(r"Response of LTI system to various frequencies")
plt.grid()
plt.show()

Xs= sgnl.lti([1, 0, 2], [1, 0, 3, 0])           #X(s) function after solving analytically
t,x= sgnl.impulse(Xs, None, np.linspace(0, 20, 1000))   #Solution for x(t)
Ys= sgnl.lti([2], [1, 0, 3, 0])                 #Y(s) function after solving analytically
t,y= sgnl.impulse(Ys, None, np.linspace(0, 20, 1000))   #Solution for y(t)

plt.figure(4)                           #Plotting x(t) & y(t) 
plt.plot(t,y, label=r"$y(t)$")
plt.plot(t,x, label=r"$x(t)$")
plt.xlabel(r"$t \to$")
plt.ylabel("Signals")
plt.title(r"$\ddot{x}+(x-y)=0$" "\n" r"$\ddot{y}+2(y-x)=0$",fontsize=7) 
plt.legend()
plt.grid()
plt.show()

L = 1e-6         #Components of the 2 -port network
C = 1e-6
R = 100
H2_s = sgnl.lti([1], [L*C, R*C, 1])   #Transfer function of the 2-port
w, mag, phase = sgnl.bode(H2_s)      #Magnitude and phase response of the system

plt.figure(5)        #Plotting the magnitude reponse of the 2-port network
plt.semilogx(w, mag)
plt.xlabel(r"$\omega \ \to$")
plt.ylabel(r"$\|H(jw)\|\ (in\ dB)$")
plt.title("Magnitude-response plot of the given 2-port network")
plt.grid()
plt.show()

plt.figure(6)       #Plotting the phase response of the 2-port network
plt.xlabel(r"$\omega \ \to$")
plt.ylabel(r"$\angle H(jw)\ (in\ ^o)$")
plt.title("Phase-response plot of the given 2-port network")
plt.semilogx(w, phase)
plt.grid()
plt.show()

t = np.linspace(0, 0.1, 10**6)     
V_i= np.cos(1e3*t) - np.cos(1e6*t)          # Input to the 2-port network
taxis, vout, rest= sgnl.lsim(H2_s, V_i, t)   #Obtaining the output of the 2-port network 

plt.figure(7)                  #Plotting the Output signal Vo(t) of the 2-port network
plt.plot(taxis, vout)
plt.xlabel(r"$t\ \to$")
plt.ylabel(r"$v_o(t)\ \to$")
plt.title(r"$v_o(t)$" " given $v_i(t)=cos(10^3t)-cos(10^6t)$")
plt.grid()
plt.show()

plt.figure(8)                #Plotting Vo(t) for t<30 us
plt.plot(taxis, vout,label= r"$v_o(t); t< 30 \ us $ ")
plt.xlim(0, 3e-5)
plt.ylim(-0.5, 0.5)
plt.xlabel(r"$t\ \to$")
plt.ylabel(r"$v_o(t)\ \to$")
plt.title(r"$v_o(t)$")
plt.grid()
plt.legend()
plt.show()