'''
		EE2703 Applied Programming Lab - 2021
				Assignment-4
	Name: SAKTHI HARISH D T
	Roll: EE19B054
'''
from matplotlib.pylab import plt          # importing the necessary modules
from scipy.linalg import lstsq
import numpy as np
import math
from sympy.abc import x
import scipy.integrate

#function that returns exp(x)
def exp_func(x):
    return(np.exp(x)) 
#function that returns cos(cos(x))
def cos_cos_func(x):
    return np.cos(np.cos(x))
#defining the x and y axis to be plotted
xlist= np.linspace(math.pi*-2,math.pi*4,1201)
xlist= xlist[:-1]
ylist1= np.array(exp_func(xlist))
xlist1_1= np.array(3*list(xlist[400:800]))
ylist1_1= np.array(exp_func(xlist1_1))
# Plot 1 showing the value of exp(x) for x ranging from -2*pi to 4*pi
plt.figure(1)
plt.grid()
plt.title(r"Plot of $exp(x)$")
plt.semilogy(xlist,ylist1,label= "exp(x)")
plt.semilogy(xlist,ylist1_1,"r--",label= "exp(t)-Periodic extension by Fourier Series")
plt.ylabel(r'$exp(x)   \longrightarrow$')
plt.xlabel(r'$x \longrightarrow$')
plt.legend()
plt.show()

ylist2= np.array(cos_cos_func(xlist)) 
ylist2_2= np.array(cos_cos_func(xlist1_1))
# Plot 2 showing the value of cos(cos(x)) for x ranging from -2*pi to 4*pi
plt.figure(2)
plt.grid()
plt.title(r"Plot of $cos(cos(x))$")
plt.plot(xlist,ylist2,label= "cos(cos(x))")
plt.plot(xlist,ylist2_2, "r--",label= "cos(cos(x) -Periodic extension by Fourier Series")
plt.legend(loc='upper right')
plt.ylabel(r'$cos(cos(x))   \longrightarrow$')
plt.xlabel(r'$x \longrightarrow$')
plt.show()

k=0
coeff_exp=np.zeros(51)

#This block calculates the Fourier Coefficients using integration
uo1= lambda x: np.exp(x)*math.cos(k*x)
coeff_exp[0]= (1/(2*math.pi))*scipy.integrate.quad(uo1,0,2*math.pi)[0]
for i in range(1,26):
    u1= lambda x: exp_func(x)*math.cos(i*x)    
    j=2*i
    coeff_exp[j-1]= (1/(math.pi))*scipy.integrate.quad(u1,0,2*math.pi)[0]
    coeff_exp[j-1]= abs(coeff_exp[j-1])
    
    v1= lambda x: exp_func(x)*math.sin(i*x)
    coeff_exp[j]= (1/(math.pi))*scipy.integrate.quad(v1,0,2*math.pi)[0]
    coeff_exp[j]= abs(coeff_exp[j])


k=0
coeff_coscos=np.zeros(51)

uo2= lambda x: cos_cos_func(x)*math.cos(k*x)
coeff_coscos[0]= (1/(2*math.pi))*scipy.integrate.quad(uo2,0,2*math.pi)[0]
for i in range(1,26):
    u2= lambda x: cos_cos_func(x)*math.cos(i*x)
    j=2*i
    coeff_coscos[j-1]= (1/(math.pi))*scipy.integrate.quad(u2,0,2*math.pi)[0]
    coeff_coscos[j-1]= abs(coeff_coscos[j-1])

    v2= lambda x: cos_cos_func(x)*math.sin(i*x)
    coeff_coscos[j]= (1/(math.pi))*scipy.integrate.quad(v2,0,2*math.pi)[0]
    coeff_coscos[j]= abs(coeff_coscos[j])

nlist1= list(range(0,51))
#Plot 3 showing the Fourier Coefficients for exp(x) calculated by integration in semilog scale
plt.figure(3)
plt.grid()
plt.semilogy(nlist1,coeff_exp,'r.',label='Coefficients for exp(x)')
plt.title(r"Coefficients of fourier series of $e^x$ on a semilog scale")
plt.ylabel(r'$Coefficients(a_n,b_n)   \longrightarrow$')
plt.xlabel(r'$n \longrightarrow$')
plt.legend()
plt.show()

#Plot 4 showing the Fourier Coefficients for exp(x) calculated by integration in loglog scale
plt.figure(4)
plt.grid()
plt.loglog(nlist1,coeff_exp,'r.',label='Coefficients for exp(x)')
plt.title(r"Coefficients of fourier series of $e^x$ on a loglog scale")
plt.ylabel(r'$Coefficients(a_n,b_n)   \longrightarrow$')
plt.xlabel(r'$n \longrightarrow$')
plt.legend()
plt.show()

#Plot 5 showing the Fourier Coefficients for cos(cos(x)) calculated by integration in semilog scale
plt.figure(5)
plt.grid()
plt.semilogy(nlist1,coeff_coscos,'r.',label='Coefficients for cos(cos(x))')
plt.title(r"Coefficients of fourier series of $cos(cos(x))$ on a semilogy scale")
plt.ylabel(r'$Coefficients(a_n,b_n)   \longrightarrow$')
plt.xlabel(r'$n \longrightarrow$')
plt.legend()
plt.show()

#Plot 6 showing the Fourier Coefficients for cos(cos(x)) calculated by integration in loglog scale
plt.figure(6)
plt.grid()
plt.loglog(nlist1,coeff_coscos,'r.',label='Coefficients for cos(cos(x))')
plt.title(r"Coefficients of fourier series of $cos(cos(x))$ on a loglog scale")
plt.ylabel(r'$Coefficients(a_n,b_n)   \longrightarrow$')
plt.xlabel(r'$n \longrightarrow$')
plt.legend()
plt.show()

#This block estimates the Fourier series coefficients using the Least Square method
x=np.linspace(0,2*math.pi,401)
x=x[:-1] 
b1= exp_func(x)
b2= cos_cos_func(x)
#This block creates the matrix A
A=np.zeros((400,51))
A[:,0]=1
for k in range(1,26):
    A[:,2*k-1]=np.cos(k*x) 
    A[:,2*k]=np.sin(k*x)

c1= lstsq(A,b1)[0]
c2= lstsq(A,b2)[0]
#Deviation of the least square estimation from the actual value
deviation_exp= np.abs(np.abs(c1)-coeff_exp)
deviation_coscos= np.abs(np.abs(c2)-coeff_coscos)
#Finding the maximum Deviation 
max_dev_exp= np.max(deviation_exp)
max_dev_coscos= np.max(deviation_coscos)
print('The maximum deviation in the coefficients computed for exp(x) by Least Square model: '+str(max_dev_exp))
print('The maximum deviation in the coefficients computed for cos(cos(x)) by Least Square model: '+str(max_dev_coscos))

#Estimated Function generated using the coefficients obtained by the least square method
exp_func_estimated= np.dot(A,c1)
cos_cos_func_estimated= np.dot(A,c2)

#Plot 7 showing the estimated coefficients for exp(x) along with actual coefficients for comparison in semilog scale
plt.figure(7)
plt.grid()
plt.semilogy(nlist1,coeff_exp,'r.',label='Coefficients for exp(x)')
plt.semilogy(nlist1,np.abs(c1),'g.',label='Estimated Coefficients for exp(x)')
plt.title(r"Coefficients of fourier series of $e^x$ on a semilogy scale")
plt.ylabel(r'$Coefficients(a_n,b_n)   \longrightarrow$')
plt.xlabel(r'$n \longrightarrow$')
plt.legend()
plt.show()

#Plot 8 showing the estimated coefficients for exp(x) along with actual coefficients for comparison in loglog scale
plt.figure(8)
plt.grid()
plt.loglog(nlist1,coeff_exp,'r.',label='Coefficients for exp(x)')
plt.loglog(nlist1,np.abs(c1),'g.',label='Estimated Coefficients for exp(x)')
plt.title(r"Coefficients of fourier series of $e^x$ on a loglog scale")
plt.ylabel(r'$Coefficients(a_n,b_n)   \longrightarrow$')
plt.xlabel(r'$n \longrightarrow$')
plt.legend()
plt.show()

#Plot 9 showing the estimated coefficients for cos(cos(x)) along with actual coefficients for comparison in semilog scale
plt.figure(9)
plt.grid()
plt.semilogy(nlist1,coeff_coscos,'r.',label='Coefficients for cos(cos(x))')
plt.semilogy(nlist1,np.abs(c2),'g.',label='Estimated Coefficients for cos(cos(x))')
plt.title(r"Coefficients of fourier series of $cos(cos(x))$ on a semilogy scale")
plt.ylabel(r'$Coefficients(a_n,b_n)   \longrightarrow$')
plt.xlabel(r'$n \longrightarrow$')
plt.legend()
plt.show()

#Plot 10 showing the estimated coefficients for cos(cos(x)) along with actual coefficients for comparison in loglog scale
plt.figure(10)
plt.grid()
plt.loglog(nlist1,coeff_coscos,'r.',label='Coefficients for cos(cos(x))')
plt.loglog(nlist1,np.abs(c2),'g.',label='Estimated Coefficients for cos(cos(x))')
plt.title(r"Coefficients of fourier series of $cos(cos(x))$ on a loglog scale")
plt.ylabel(r'$Coefficients(a_n,b_n)   \longrightarrow$')
plt.xlabel(r'$n \longrightarrow$')
plt.legend()
plt.show()

# Plot 11 showing the estimated function exp(x) along with actual function for comparison
plt.figure(11)
plt.semilogy(xlist,ylist1,label= "exp(x)")
plt.semilogy(xlist,ylist1_1,"r--",label= "exp(t)-Periodic extention by Fourier Series")
plt.semilogy(x,exp_func_estimated,'g.',label= "Estimated exp(x)")
plt.legend()
plt.grid()
plt.title(r"Plot of $exp(x)$ along with estimated function")
plt.ylabel(r'$exp(x)   \longrightarrow$')
plt.xlabel(r'$x \longrightarrow$')
plt.show()

#Plot 12 showing the estimated function cos(cos(x)) along with actual function for comparison
plt.figure(12)
plt.grid()
plt.plot(xlist,ylist2,label= "cos(cos(x))")
plt.plot(xlist,ylist2_2, "r--",label= "cos(cos(x) -Periodic extension Fourier Series")
plt.plot(x,cos_cos_func_estimated,'g.',label='Estimated cos(cos(x))')
plt.legend(loc='upper right')
plt.title(r"Plot of $cos(cos(x))$ along with estimated function")
plt.ylabel(r'$cos(cos(x))   \longrightarrow$')
plt.xlabel(r'$x \longrightarrow$')
plt.show()