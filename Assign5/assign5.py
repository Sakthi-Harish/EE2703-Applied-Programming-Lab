'''
		EE2703 Applied Programming Lab - 2021
				Assignment-5: Resistor problem(Laplace equation)
	Name: SAKTHI HARISH D T
	Roll: EE19B054
'''
from matplotlib.pylab import plt  #importing the required libraries
import mpl_toolkits.mplot3d.axes3d as p3
import sys
import numpy as np
from scipy.linalg import lstsq

args= sys.argv  #object for the command-line arguments

side= 1  #length of each side of the square plate 

if(len(args)!=5):    #Checking if File name is given or not (or) if too many arguments are given 
    if(len(args)==1):
        Nx= 25 # size along x
        Ny= 25 # size along y
        radius= 0.35  # radius of central lead
        Niter= 1500 #Number of iterations to perform
    else:
        print("\nRequired Usage: Nx Ny radius(in cm) N_iter")
        exit()
else:
    Nx= int(args[1])
    Ny= int(args[2])
    radius= float(args[3])
    Niter= int(args[4])

phi= np.zeros((Nx,Ny))    #this block determines the points to be kept at 1 volts till the end
x= np.linspace(-side/2,side/2,Nx)
y= np.linspace(-side/2,side/2,Ny)
Y,X= np.meshgrid(y,x) 
ii= np.where(X**2+Y**2<= (radius)**2) #checking the location of points whose distance from centre is less than radius
phi[ii]= 1  

plt.figure()   #plotting the contour of the potential before iteration
plt.contourf(Y,X,phi)
plt.plot(y[ii[0]],x[ii[1]],'ro',label='1 volt lead')
plt.title('Contour plot of the potential')
plt.colorbar(ax= plt.axes(), orientation='vertical')
plt.xlabel(r'$X \longrightarrow$')
plt.ylabel(r'$Y \longrightarrow$')
plt.legend()
plt.grid()
plt.show()

errors=np.zeros(Niter)    #This block updates the value of potential at each point in the plate and keeps track of the error in each iteration
for i in range(Niter):
    oldphi= phi.copy()
    phi[1:-1,1:-1]= 0.25*(phi[1:-1,0:-2]+phi[1:-1,2:]+phi[0:-2,1:-1]+phi[2:,1:-1])
    phi[1:-1,0]= phi[1:-1,1] 
    phi[1:-1,-1]= phi[1:-1,-2] 
    phi[0,:]= phi[1,:] 
    phi[ii]= 1.0
    errors[i]= (abs(oldphi-phi)).max()


x_list=np.linspace(0,Niter,Niter)  #Fitting the errors using the Least Squares Approach
M=np.zeros((Niter,2))
x_list1=np.linspace(1,Niter+1,1500)
M[:,0]=1
M[:,1]=(x_list1[0:])
coeff1=lstsq(M,np.log(errors[:]))[0]#least squares
coeff2=lstsq(M[501:],np.log(errors[501:]))[0]

log_A1=coeff1[0]
B1=coeff1[1]
error1=np.exp(log_A1)*np.exp(B1*(x_list1))  #Fit 1
print(np.exp(log_A1),B1)

log_A2=coeff2[0]
B2=coeff2[1]
error2=np.exp(log_A2)*np.exp(B1*(x_list1)) #Fit 2
print(np.exp(log_A2),B2)

plt.figure()   #Semilogy plot of the error vs No. of iterations
plt.semilogy(x_list[0:-1:50],errors[0:-1:50],'ro--',label='error')
plt.legend()
plt.xlabel('Number of iterations')
plt.ylabel('$log(error)$')
plt.grid()
plt.title('Semilogy Plot of error vs number of iterations')
plt.show()

plt.figure()   #Log-Log plot of the error vs No. of iterations
plt.loglog(x_list[0:-1:50],errors[0:-1:50],'ro--',label='error')
plt.legend()
plt.xlabel('Number of iterations')
plt.ylabel('$log(error)$')
plt.grid()
plt.title('Log-Log Plot of error vs number of iterations')
plt.show()

plt.figure()    #Semilogy plot of the error vs No. of iterations along with 2 Least squares model Fits
plt.semilogy(x_list[0:-1:50],errors[0:-1:50],'b',label='actual error')
plt.semilogy(x_list[0:-1:50],error1[0:-1:50],'rx',label='fit 1(using all points)')
plt.semilogy(x_list[501:-1:50],error2[501:-1:50],'g+',label='fit 2(above 500)')
plt.legend()
plt.xlabel('Number of iterations')
plt.ylabel('$log(error)$')
plt.grid()
plt.title('Semilogy Plot of error vs number of iterations along with 2 fitted models')
plt.show()

fig1=plt.figure(4)   # This plot shows the 3D surface plot of the potential
ax=p3.Axes3D(fig1) 
x=np.linspace(side/2,-side/2,Nx)
y=np.linspace(side/2,-side/2,Ny)
Y,X=np.meshgrid(y,x)  
plt.title('The 3-D surface plot of the potential')
surf = ax.plot_surface(X, Y, phi.T, rstride=1, cstride=1,cmap='jet')
plt.show()

x=np.linspace(side/2,-side/2,Nx)   #Contour plot of the potential after the iterations
y=np.linspace(side/2,-side/2,Ny)
Y,X=np.meshgrid(y,x)
plt.contourf(X,Y,phi.T)
plt.colorbar(ax= plt.axes(), orientation='vertical')
plt.plot(y[ii[0]],x[ii[1]],'ro',label='1 volt lead')
plt.title('Contour plot of the potential')
plt.legend()
plt.show()

x=np.linspace(-side/2,side/2,Nx)
y=np.linspace(-side/2,side/2,Ny)
Y,X=np.meshgrid(y,x)
Jx=np.zeros((Nx,Ny))
Jy=np.zeros((Nx,Ny))
Jx[1:-1,1:-1]=0.5*(phi[1:-1,0:-2]-phi[1:-1,2:])
Jy[1:-1,1:-1]=0.5*(phi[0:-2,1:-1]-phi[2:,1:-1])

plt.figure()    #Vector plot of the currents
plt.quiver(x,y,Jx[::-1,:],-Jy[::-1,:],scale=4)
plt.plot(y[ii[0]],x[ii[1]],'ro',label='1 volt lead')
plt.title("Current plot with magnitudes scaled to 1/4 th of it's value")
plt.legend()
plt.show()

#This block evaluates the temperature of the plates with the given boundary conditions
k= 1    #k value(Thermal conductivity)
sigma= 1  #sigma(Electrical conductivity)
c= (Jx[1:-1,1:-1]**2+ Jy[1:-1,1:-1]**2)/(sigma*k) #particular soln constant

temp= np.zeros((Nx,Ny)) #Let us define the boundary conditions here(as given in the question pdf)
temp[ii]= 300       
temp[-1,:]= 300     

for k in range(Niter):     #This block updates the value of Temperature
    temp[1:-1,1:-1]= 0.25*((temp[1:-1,0:-2]+temp[1:-1,2:]+temp[0:-2,1:-1]+temp[2:,1:-1])+c)
    temp[1:-1,0]= temp[1:-1,1] 
    temp[1:-1,-1]= temp[1:-1,-2]
    temp[0,:]= temp[1,:] 
    temp[ii]= 300
        
fig1= plt.figure(4)     #This block plots the 3D surface plot of the temperature
ax= p3.Axes3D(fig1) 
x=np.linspace(-side/2,side/2,Nx)
y=np.linspace(-side/2,side/2,Ny)
Y,X= np.meshgrid(y,x) 
plt.title('The 3-D surface plot of the Temperature')
surf = ax.plot_surface(Y, X, temp.T, rstride=1, cstride=1,cmap='jet')
plt.show()


