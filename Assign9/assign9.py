'''
		EE2703 Applied Programming Lab - 2021
		Assignment-9: The Digital Fourier Transform
	Name: SAKTHI HARISH D T
	Roll: EE19B054
'''
import matplotlib.pyplot as plt     #importing the required libraries 
import numpy as np
import numpy.fft as fft

x= np.random.rand(128)          #creating a list of random numbers
X= fft.fft(x)               #FFT of the random numbers function x
y= fft.ifft(X)              #Inverse FFT of the FFT of x,,(i.e) computed value of x
t= np.linspace(-64, 63, 129); t= t[:-1]     
print(r'Absolute Maximum error b/w "Actual x" and "ifft(fft(x))" : ', max(np.abs(y-x)))   # Printing the maximum value of error between the two 'x' values
plt.figure(0)       #This block plots the actual values and computed values of x 
plt.plot(t, x, 'b.', label='$Actual-x$', lw=2)
plt.plot(t, np.abs(y), 'g', label='$Computed-x$', lw=2)
plt.xlabel(r'$t\ \longrightarrow$')
plt.ylabel(r'$Actual\ x\ and \ Computed \ x \longrightarrow$')
plt.grid()
plt.legend()
plt.title('Plots of Actual x and Computed x ')
#plt.savefig('Fig0.png')
plt.show()

x = np.linspace(0, 2*np.pi, 129); x = x[:-1]        # This block plots the spectrum of sin(5x)
y = np.sin(5*x)
Y = (1/128)*fft.fftshift(fft.fft(y))                #FFT of sin(5x)
w= np.linspace(-64, 63, 128)                    #frequency vector
fig1 = plt.figure(1)                        
fig1.suptitle(r'Spectrum of $sin(5t)$')
plt.subplot(211)            #Plotting magnitude spectrum of sin(5x)
plt.plot(w, np.abs(Y), lw=2)
plt.xlim([-10, 10])
plt.ylabel(r'$\|Y\|$',size=16)
plt.grid()
plt.subplot(212)            #Plotting the phase spectrum of sin(5x)
ii= np.where(np.abs(Y) > 1e-3)      #Plotting points only where magnitude is significant
plt.plot(w[ii], np.angle(Y[ii]), 'go', lw=2)
plt.xlim([-10, 10])
plt.ylim([-2, 2])
plt.ylabel(r'$\angle Y$',size=16)
plt.xlabel(r'$\omega  \longrightarrow$',size=16)
plt.grid()
#plt.savefig('Fig1.png')
plt.show()

t= np.linspace(-4*np.pi, 4*np.pi, 513); t= t[:-1]           # This block plots the spectrum of (1+0.1*cos(t))*cos(10t)
y = (1+0.1*np.cos(t))*np.cos(10*t)
Y = fft.fftshift(fft.fft(y))/512.0          #FFT of y
w = np.linspace(-64, 64, 513); w = w[:-1]       #frequency vector
fig2 = plt.figure(2)        
fig2.suptitle(r'Spectrum of $\left(1+0.1\cos\left(t\right)\right)\cos\left(10t\right)$')
plt.subplot(211)            #Plotting magnitude spectrum of y
plt.plot(w, np.abs(Y), lw=2)
plt.xlim([-15, 15])
plt.ylabel(r'$\|Y\|$')
plt.grid()
plt.subplot(212)            #Plotting phase spectrum of y
plt.xlim([-15, 15])
plt.ylim([-2, 2])
plt.ylabel(r'$\angle Y$')
plt.xlabel(r'$\omega  \longrightarrow$')
jj= np.where(np.abs(Y)> 1e-3)
plt.plot(w[jj], np.angle(Y[jj]), 'go', lw=2)
plt.grid()
#plt.savefig('Fig2.png')
plt.show()

t= np.linspace(-4*np.pi, 4*np.pi, 513); t= t[:-1]       #This block plots the spectrum of sin^3(t)
y = (np.sin(t))**3
Y = fft.fftshift(fft.fft(y))/512.0          #FFT of sin^3(t)
w = np.linspace(-64, 64, 513); w = w[:-1]       #Frequency vector
fig2 = plt.figure(3)
fig2.suptitle(r'Spectrum of $sin^3(t)$')
plt.subplot(211)                #Magnitude spectrum of sin^3(t) 
plt.plot(w, np.abs(Y), lw=2)
plt.xlim([-15, 15])
plt.ylabel(r'$\|Y\|$')
plt.grid()
plt.subplot(212)                #Phase spectrum of sin^3(t)
plt.xlim([-15, 15])
plt.ylim([-2, 2])
plt.ylabel(r'$\angle Y$')
plt.xlabel(r'$\omega  \longrightarrow$')
jj= np.where(np.abs(Y)> 1e-3)
plt.plot(w[jj], np.angle(Y[jj]), 'go', lw=2)
plt.grid()
#plt.savefig('Fig3.png')
plt.show()

t= np.linspace(-4*np.pi, 4*np.pi, 513); t= t[:-1]           #This block plots the spectrum of cos^3(t)
y = (np.cos(t))**3
Y = fft.fftshift(fft.fft(y))/512.0          #FFT of cos^3(t)
w = np.linspace(-64, 64, 513); w = w[:-1]   #Frequency vector
fig2 = plt.figure(4)
fig2.suptitle(r'Spectrum of $cos^3(t)$')
plt.subplot(211)            #Magnitude spectrum of cos^3(t)
plt.plot(w, np.abs(Y), lw=2)
plt.xlim([-15, 15])
plt.ylabel(r'$\|Y\|$')
plt.grid()
plt.subplot(212)            #Phase spectrum of cos^3(t)
plt.xlim([-15, 15])
plt.ylim([-2, 2])
plt.ylabel(r'$\angle Y$')
plt.xlabel(r'$\omega  \longrightarrow$')
jj= np.where(np.abs(Y)> 1e-3)
plt.plot(w[jj], np.angle(Y[jj]), 'go', lw=2)
plt.grid()
#plt.savefig('Fig4.png')
plt.show()

t= np.linspace(-4*np.pi, 4*np.pi, 513); t= t[:-1]           #This block plots the spectrum of cos(20t+5*cos(t))
y = np.cos((20*t)+(5*np.cos(t)))
Y = fft.fftshift(fft.fft(y))/512.0              #FFT of cos(20t+5*cos(t))
w = np.linspace(-64, 64, 513); w = w[:-1]       #Frequency vector
fig2 = plt.figure(5)
fig2.suptitle(r'Spectrum of $ cos(20t\ +\ 5cos(t))$')
plt.subplot(211)        #Magnitude spectrum of cos(20t+5*cos(t))
plt.plot(w, np.abs(Y), lw=2)
plt.xlim([-30, 30])
plt.ylabel(r'$\|Y\|$')
plt.grid()
plt.subplot(212)        #Phase spectrum of cos(20t+5*cos(t))
plt.xlim([-30, 30])
plt.ylabel(r'$\angle Y$')
plt.xlabel(r'$\omega  \longrightarrow$')
jj= np.where(np.abs(Y)> 1e-3)
plt.plot(w[jj], np.angle(Y[jj]), 'go', lw=2)
plt.grid()
#plt.savefig('Fig5.png')
plt.show()

t= np.linspace(-1*4*np.pi, 4*np.pi, 513); t= t[:-1]     #This block plots the spectrum of Gaussian function 
y = np.exp(-1*(t**2)/2)
Y = fft.fftshift(fft.fft(y))*4/512.0        #FFT of Gaussian(also a Gaussian)
w = np.linspace(-64, 64, 513); w = w[:-1]       #Frequency vector
fig2 = plt.figure(6)
fig2.suptitle(r'Spectrum of $e^{-t^2/2}$')
plt.subplot(211)        #Magnitude spectrum of Gaussian
plt.plot(w, np.abs(Y),color='blue', label='Computed spectrum',lw=2)
plt.plot(w,abs(np.exp(-(w**2)/2)/np.sqrt(2*np.pi)),'g.',label= 'Actual spectrum', lw=2)
plt.xlim([-8, 8])
plt.ylabel(r'$\|Y\|$')
plt.legend()
plt.grid()
plt.subplot(212)            #Phase spectrum of Gaussian
plt.xlim([-8, 8])
plt.ylim([-2, 2])
plt.ylabel(r'$\angle Y$')
plt.xlabel(r'$\omega  \longrightarrow$')
plt.plot(w, np.angle(Y),'bo',lw=2)
plt.plot(w, np.angle(np.exp(-(w**2)/2)/np.sqrt(2*np.pi)),'g.',lw=2)
plt.grid()
#plt.savefig('Fig6.png')
plt.show()

mean_error = np.mean(np.abs(np.exp(-(w**2)/2)/np.sqrt(2*np.pi) - Y))		#We calculate the mean error between actual DFT of Gaussian and the calculated one
print(r'Magnitude of mean error between actual and computed values of the Gaussian: ', mean_error) 
