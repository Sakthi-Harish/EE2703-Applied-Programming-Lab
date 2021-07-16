'''
		EE2703 Applied Programming Lab - 2021
		Assignment-8:Analysis of Circuits using Laplace Transform, Sympy
	Name: SAKTHI HARISH D T
	Roll: EE19B054
'''
import numpy as np          #importing required libraries
import scipy.signal as sgnl
import matplotlib.pyplot as plt
import sympy as sp

def lowPass(R1, R2, C1, C2, G, Vi):     #function to return Voltage values for LowPass Filter
    s= sp.symbols('s')
    A= sp.Matrix([[0, 0, 1, -1/G],
                  [-1/(1+s*R2*C2), 1, 0, 0],
                  [0, -G, G, 1],
                  [-1/R1-1/R2-s*C1, 1/R2, 0, s*C1]])
    b= sp.Matrix([0,
                  0,
                  0,
                  -Vi/R1])
    V= A.inv()*b
    return (A,b,V)

def highPass(R1, R3, C1, C2, G, Vi):    #function to return Voltage values for HighPass Filter
    s= sp.symbols('s')
    A= sp.Matrix([[0, -1, 0, 1/G],
                  [s*C2*R3/(s*C2*R3+1), 0, -1, 0],
                  [0, G, -G, 1],
                  [(-1*s*C2)-(1/R1)-(s*C1), 0, s*C2, 1/R1]])

    b= sp.Matrix([0,
                  0,
                  0,
                  -Vi*s*C1])
    V= A.inv()*b
    return (A,b,V)

s= sp.symbols('s')
A,b,V= lowPass(10000, 10000, 1e-9, 1e-9, 1.586, 1)  
t = np.linspace(0, 0.1, 10**6)
Vo= V[3]
n,d= sp.fraction(Vo)    #this block converts Vo to list 
n= sp.Poly(n, s)
d= sp.Poly(d, s)
n_coeff= n.all_coeffs()
d_coeff= d.all_coeffs()
n_coeff= [float(i) for i in n_coeff]
d_coeff= [float(i) for i in d_coeff]
Vo_s= sgnl.lti(n_coeff,d_coeff)     #Defining the LTI system

#Question 1
time, voStep = sgnl.step(Vo_s, None, np.linspace(0, 0.001, 10**4))      #Plotting step response of the Lowpass filter
plt.figure(1)
plt.plot(time, voStep)
plt.title(r'Q1. Step Response of Lowpass filter')
plt.xlabel(r'$t\ \longrightarrow$')
plt.ylabel(r'$V_o(t)\ \longrightarrow$')
plt.grid(True)
plt.show()

#Question 2
v_i= (np.sin(2e3*np.pi*t)+np.cos(2e6*np.pi*t))*np.heaviside(t,1)    #input voltage suppied to the circuit
plt.figure(2)
plt.plot(t, v_i,label=r'$V_i(t)$')
time, v_o, rest = sgnl.lsim(Vo_s, v_i, t)  #Plotting the output voltage using signal.lsim
plt.plot(time, v_o,label=r'$V_o(t)$')
plt.title(r'$(Q.2) V_o(t)$ for $V_i(t)=(sin(2x10^3\pi t)+cos(2x10^6\pi t))u(t)$ for Lowpass filter')
plt.xlabel(r'$t\ \to$')
plt.ylabel(r'$Signals$')
plt.xlim(0, 1e-3)
plt.grid(True)
plt.legend()
plt.show()

#Question 3
A,b,V= highPass(10000, 10000, 1e-9, 1e-9, 1.586, 1)     #calling the highpass filter function
Vo2= V[3]
n,d= sp.fraction(Vo2)       #this block converts Vo2 to list
n= sp.Poly(n, s)
d= sp.Poly(d, s)
n_coeff= n.all_coeffs()
d_coeff= d.all_coeffs()
n_coeff= [float(i) for i in n_coeff]
d_coeff= [float(i) for i in d_coeff]
Vo_s= sgnl.lti(n_coeff,d_coeff)     #Defining the LTI system

w= np.linspace(0,10e6,10**6)        #Plotting the magnitude response of the system 
ss= 1j*w
hf= sp.lambdify(s,Vo2,'numpy')
v= hf(ss)
plt.figure(3)
plt.loglog(w,abs(v),lw=2)
plt.title(r'(Q.3).Bode Magnitude Plot of Transfer function of highpass filter')
plt.grid(True)
plt.ylabel(r'$20log(\|H(j\omega)\|)$')
plt.xlabel(r'$\omega \ \longrightarrow$')
plt.show()

v_i= (np.sin(2e3*np.pi*t)+np.cos(2e6*np.pi*t))*np.heaviside(t,1)        #input voltage supplied to circuit
plt.figure(4)
plt.plot(t, v_i,label=r'$V_i(t)$')
time, v_o, rest = sgnl.lsim(Vo_s, v_i, t)           #Plotting output voltage of Highpass filter for the given input
plt.plot(time, v_o,label=r'$V_o(t)$')
plt.title(r'(Q.3)$V_o(t)$ for $V_i(t)=(sin(2x10^3\pi t)+cos(2x10^6\pi t))u(t)$ for HPF')
plt.xlim(0, 1e-3)
plt.grid(True)
plt.legend()
plt.show()

#Question 4
Vi_damp_low_freq = (np.sin(1e3*np.pi*t))*np.exp(-10*t)*np.heaviside(t, 1)       #input damped sinusoid voltage with low frequency 
Vi_damp_high_freq = (np.sin(1e6*np.pi*t))*np.exp(-1e4*t)*np.heaviside(t, 1)     #input damped sinusoid voltage with high frequency

# Output for low frequency damped sinusoid
time, Vo_damp_low_freq, rest = sgnl.lsim(Vo_s, Vi_damp_low_freq, t)
plt.figure(5)
plt.plot(t,Vi_damp_low_freq,label=r'$V_i(t)$')
plt.plot(time, Vo_damp_low_freq,label=r'$V_o(t)$')
plt.title(r'(Q.4) $V_o(t)$ for $V_i(t)=sin(1000\pi t)e^{-10t}u(t)$ for HPF(Low freq Damped input)')
plt.xlabel(r'$t\ \to$')
plt.ylabel(r'$V_o(t)\ \to$')
plt.grid(True)
plt.legend()
plt.show()

# Output for high frequency damped sinusoid
time, Vo_damp_high_freq, rest = sgnl.lsim(Vo_s, Vi_damp_high_freq, t)
plt.figure(6)
plt.plot(t,Vi_damp_high_freq,label=r'$V_i(t)$')
plt.plot(time, Vo_damp_high_freq,label=r'$V_o(t)$')
plt.title(r'(Q.4) $V_o(t)$ for $V_i(t)=sin(10^6\pi t)e^{-10000t}u(t)$ for HPF(High freq Damped input)')
plt.xlabel(r'$t\ \to$')
plt.ylabel(r'$V_o(t)\ \to$')
plt.xlim(0,1e-4)
plt.grid(True)
plt.legend()
plt.show()

#Question 5
time, voStep, rest= sgnl.lsim(Vo_s, np.heaviside(t,1), t)       #response of the Highpass filter for Unit Step input(Unit step response)
plt.figure(7)
plt.plot(time, voStep,label=r'$V_o(t)$')
plt.title(r'Q5.Response of Highpass filter for Unit Step')
plt.xlabel(r'$t\ \longrightarrow$')
plt.ylabel(r'$V_o(t)\ \longrightarrow$')
plt.xlim(-1e-4,1e-3)
plt.grid(True)
plt.legend()
plt.show()