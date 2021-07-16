'''
		EE2703 Applied Programming Lab - 2021
				Assignment-6: 1-D simulation of tube-light
	Name: SAKTHI HARISH D T
	Roll: EE19B054
'''
import sys                #importing the required libraries
import numpy as np
from matplotlib.pylab import plt 

args= sys.argv   #list containing the commandline arguments

if(len(args)!=7):    #Checking if File name is given or not (or) if too many arguments are given 
    if(len(args)==1):
        n= 100       #spatial grid size.
        M= 5         #number of electrons injected per turn.
        nk= 500      #number of turns to simulate.
        u0= 5        #threshold velocity.
        p= 0.25      #probability that ionization will occur
        Msig= 2      #std. dev for random number generation
    else:
        print("\nRequired Usage: n(grid size) M(no. of electrons per turn) nk(no. of turns to simulate) u0(Velocity) p(probability)")
        exit()
else:
    n= int(args[1])
    M= int(args[2])
    nk= int(args[3])
    u0= int(args[4])
    p= float(args[5])
    Msig= float(args[5])

xx= np.zeros(n*M)  # vector for electron position
u= np.zeros(n*M)   # vector for electron velocity
dx= np.zeros(n*M)  # vector for displacement in current turn

I= []      #lists of Light intensity, position and Velocity
X= []
V= []

for k in range(nk-1):
    ii= np.where(xx>0)       #finding the indices of positions greater than zero
    dx[ii]= u[ii]+ 0.5        #Updating the vectors
    xx[ii]= xx[ii]+ dx[ii]     
    u[ii]= u[ii]+ 1           
    
    anode_hit= np.where(xx[ii]>n)     #Finding the indices of electrons that reached anode
    xx[ii[0][anode_hit]]= 0       #Updating the values after hitting the anode
    u[ii[0][anode_hit]]= 0
    dx[ii[0][anode_hit]]= 0

    kk= np.where(u>= u0)       #Finding the indices of energetic electrons
    ll= np.where(np.random.rand(len(kk[0]))<= p)     #Vector of indices, containing indices of kk  
    kl= kk[0][ll]              #Vector of indices of kk np.where collision occurs
    u[kl]= 0               #Updating the velocity of electrons suffering collision

    xx[kl]= xx[kl]- (dx[kl]* np.random.rand(len(kl)))    #randomly deciding np.where the collision took place
    I.extend(xx[kl].tolist())
    m= int(np.random.rand()*Msig)+ M
    
    free= np.where(xx==0)       #Finding free spaces in the grid
    n_inject= min((n*M)-len(free),m)
    
    xx[free[:n_inject]]= 1    #Updating the values of vectors corresponding to the injected electrons
    u[free[0][:n_inject]]= 0   # (i.e) position= 1; velocity= 0 ; displacement= 0
    dx[free[0][:n_inject]]= 0         
    X.extend(xx.tolist())
    V.extend(u.tolist())

plt.figure(1)                   #Plotting 'Electron density' w.r.t 'x' for the given value of velocity and probability  
plt.hist(X,bins= np.arange(0,n+1,0.5),rwidth=0.75,color='blue')
plt.title('Number of Electrons vs $x$ with $u_0=$%f and p=%f'%(u0,p))
plt.xlabel(r'$x \longrightarrow$')
plt.ylabel(r'Number of electrons $\longrightarrow$')
plt.show()

plt.figure(2)                   #Plotting 'Light Intensity' w.r.t 'x' for the given value of velocity and probability 
histogram= plt.hist(I,bins= np.arange(0,n+1,0.5),rwidth=0.75,color='red')
plt.title('Intensity histogram with $u_0=$%f and p=%f'%(u0,p))
plt.xlabel(r'$x \longrightarrow$')
plt.ylabel(r'Intensity $\longrightarrow$')
plt.show()

plt.figure(3)                   #Plotting 'Electron Phase space'
plt.plot(X,V,'g.')
plt.title('Electron Phase Space with $u_0=$%f and p=%f'%(u0,p))
plt.xlabel('$x$')
plt.ylabel('Velocity-$v$')
plt.show()

xpos=0.5*(histogram[1][0:-1]+ histogram[1][1:])    #Printing the light intensity table
print('Intensity Data: \n xpos \t count \n ')

for i in range(len(xpos)):
    print('%.2f \t %f'%(xpos[i],histogram[0][i]))
