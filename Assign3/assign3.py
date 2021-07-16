"""         Assignment 3: Fitting Data to model
        
    Name: Sakthi Harish D T
    Roll.no. EE19B054

#-This code loads data from a file "fitting.dat" and does fitting of the data to a model(Least Squares Method). 
#-The plots are generated automatically when running the code.
"""


from matplotlib.pylab import plt          # importing the necessary modules
from scipy.linalg import lstsq
import numpy as np
import scipy.special as sp
from sklearn.metrics import mean_squared_error


#Python function to calculate the value g(t,A,B)
def g(t,A,B):
    g= A* sp.jv(2,t) + B* t
    return g
try:
    #(Q.2).Loading the data from the data file and storing it as numpy array
    df= np.loadtxt("fitting.dat",delimiter=" ",unpack= True)
    columns= np.array(df[:])
    t= np.array(columns[0])

    #(Q.3)Creating a list containing the standard deviation for the noise
    noise_sig= np.logspace(-1,-3,9)
    noise_sig= np.around(noise_sig, 3)

    #(Q.4).Plotting the columns in the data file for different Standard deviations and also comparing with the True value
    plt.figure(0)
    for i in range(1,len(columns)):
        plt.plot(t, columns[i],label=r"$\sigma_%d = %.3f$"%(i, noise_sig[i-1]))
    Ao= 1.05; Bo= -0.105 
    go= g(t,Ao,Bo)
    plt.plot(t, go, label="True Value",color= "black")
    plt.xlabel(r'$t$   $\longrightarrow$',size=12)
    plt.ylabel(r'$f(t)+noise \longrightarrow$',size=12)
    plt.title('(Q.4) Data to be fitted to theory',size=18)
    plt.legend()
    plt.grid(True)
    plt.show()

    #(Q.5).Plotting the Error in data no.1 from the actual data
    plt.figure(1)
    plt.title(r'(Q.5) Data points for $\sigma$ = 0.10 along with exact function')
    plt.xlabel(r'$t$   $\longrightarrow$',size=20)
    plt.plot(t,go)
    plt.grid(True)
    plt.errorbar(t[::5],columns[1][::5],0.1,fmt='ro')
    plt.legend(labels=[r'$f(t)$','$Errorbar$'])
    plt.show()


    J_column= sp.jv(2,t)
    M= np.c_[J_column,t]
    po= np.array([Ao,Bo])
    g1= np.dot(M,po)
    comparison= g1 == go

    if(comparison.all()):
        print("(Q.6) g(t,Ao,Bo) is equal to True value. Hence, verified.")
    else:
        print("(Q.6) g(t,Ao,Bo) is not equal to True value.")

    E= np.zeros(shape= (21,21))
    #Finding the value of Epsilon[i][j] by iterating the value of A and B
    for i in range(0,21,1):
        A= i/10
        for j in range(0,21,1):
            B=-0.2+(j/100)
            p= np.array([A,B])
            
            E[i][j]= mean_squared_error(np.array(columns[1]), g(t,A,B))
    xlist= np.linspace(0,2,21)
    ylist= np.linspace(-0.2,0,21)
    X,Y= np.meshgrid(xlist,ylist)
    #(Q.8) Plotting a Contour plot for the Epsilon[i][j] values for different A and b values
    plt.figure(2)
    plt.title(r'(Q.8) Contour plot for $\epsilon_{ij}$',size=18)
    plt.xlabel(r'A  $\longrightarrow$',size=20)
    plt.ylabel(r'B  $\longrightarrow$',size=20)
    cp= plt.contour(X,Y,E,20)
    plt.clabel(cp,cp.levels[1:8], inline= True, fontsize= 8)
    plt.plot(1.05,-0.105,'ro',label= "Exact location")
    plt.legend()
    plt.show()
    #(Q.9,Q.10) Using the Least Squares Method to fit the data to the model  
    err_A= np.zeros(9)
    err_B= np.zeros(9)
    for i in range(1,len(columns)):
        p,resid,rank,sig=lstsq(M,np.array(columns[i]))
        error_A= abs(p[0]-Ao)
        error_B= abs(p[1]-Bo)
        err_A[i-1]= error_A
        err_B[i-1]= error_B
    #(Q.10)Plotting the Mean Square Error in finding the best model for each column of the data file(total 9 columns) for different noise  
    plt.figure(3)
    plt.grid(True)
    plt.plot(noise_sig,err_A,'ro--',label=r'$A_{err}$')
    plt.plot(noise_sig,err_B,'go--',label=r"$B_{err}$")
    plt.title(r'(Q.10) Variation of Error with Noise',size=18)
    plt.xlabel(r'$Noise$ $Standard$ $Deviation$ $\longrightarrow$',size=12)
    plt.ylabel(r'$MS$ $error$  $\longrightarrow$',size=12)
    plt.legend()
    plt.show()
    #(Q.11)Plotting the Loglog plot of the above plot for better understanding of its behaviour
    plt.figure(4)
    plt.grid(True)
    plt.loglog(noise_sig,err_A,'ro',label=r'$A_{err}$')
    plt.errorbar(noise_sig,err_A, np.std(err_A), fmt= 'ro')
    plt.loglog(noise_sig,err_B,'go',label=r"$B_{err}$")
    plt.errorbar(noise_sig,err_B, np.std(err_B), fmt= 'go')
    plt.title(r'(Q.11) Variation of Error with Noise',size=18)
    plt.xlabel(r'$\sigma_n$ $\longrightarrow$',size=12)
    plt.ylabel(r'$MS$ $error$  $\longrightarrow$',size=12)
    plt.legend()
    plt.show()
except IOError:
    print("This file doesn't exist (or) is in unsupported format.")
#end


        