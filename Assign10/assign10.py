'''
		EE2703 Applied Programming Lab - 2021
		Assignment-10: Spectra of non-periodic signals
	Name: SAKTHI HARISH D T
	Roll: EE19B054
'''
import numpy as np          #importing the required libraries
import numpy.fft as fft
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

fig_no= 0       #variable to store the index of plots  

#function to plot the Magnitude and Phase spectrum of a signal 
def spectrum_plot(w,Y,title, magStyle='b-', phaseStyle='ro', xLimit=None, yLimit=None, showFig=False, saveFig=True, blockFig=False):
    global fig_no
    plt.figure(fig_no)
    plt.suptitle(title)
    plt.subplot(211)
    plt.grid()
    plt.plot(w,abs(Y),magStyle, lw=2)
    plt.ylabel(r"$\|Y\|$")
    if (xLimit):
        plt.xlim(xLimit)
    if (yLimit):
        plt.ylim(yLimit)
    plt.subplot(212)
    plt.grid()
    plt.plot(w,np.angle(Y),phaseStyle, lw=2)
    plt.xlim(xLimit)
    plt.ylabel(r"$\angle Y$")
    plt.xlabel(r"$\omega\ \to$")
    plt.show()
    fig_no += 1

#Question 1: Working through the example codes
t= np.linspace(-1*np.pi, np.pi, 65); t= t[:-1]      #Spectrum of sin(sqrt(2)*t) without Hamming window
dt= t[1]-t[0]
fmax= 1/dt
y= np.sin(np.sqrt(2)*t)
y[0]= 0
y= fft.fftshift(y)
Y= fft.fftshift(fft.fft(y))/64.0
w= np.linspace(-1*np.pi*fmax, np.pi*fmax, 65)[:-1]
spectrum_plot(w,Y,r"Spectrum of $sin(\sqrt{2}t)$",xLimit=[-10, 10])

t= np.linspace(-4*np.pi, 4*np.pi, 257);t=t[:-1]     #Spectrum of sin(sqrt(2)*t) with Hamming window
dt= t[1]-t[0]; fmax= 1/dt
n= np.arange(256)
wnd= fft.fftshift(0.54+0.46*np.cos(2*np.pi*n/(n.size-1)))       #Hamming Window
y= np.sin(np.sqrt(2)*t)
y= y*wnd
y[0]= 0
y= fft.fftshift(y)
Y = fft.fftshift(fft.fft(y))/256.0
w = np.linspace(-np.pi*fmax, np.pi*fmax, 257);w= w[:-1]
spectrum_plot(w,Y,r"Spectrum of $sin(\sqrt{2}t) * w(t)$",magStyle='b-o',xLimit=[-4, 4])

#Question 2: Spectrum of cos^3(0.86*t)
t= np.linspace(-1*np.pi, np.pi, 65); t= t[:-1]          #Spectrum of cos^3(0.86*t) without Hamming window
dt= t[1]-t[0]
fmax= 1/dt
y= np.cos(0.86*t)**3
y[0]= 0
y= fft.fftshift(y)
Y= fft.fftshift(fft.fft(y))/64.0
w= np.linspace(-1*np.pi*fmax, np.pi*fmax, 65)[:-1]
spectrum_plot(w,Y,r"Spectrum of $cos^3(0.86t)$",xLimit=[-10, 10])

t= np.linspace(-4*np.pi, 4*np.pi, 257);t=t[:-1]         #Spectrum of cos^3(0.86*t) with Hamming window
dt= t[1]-t[0]; fmax= 1/dt
n= np.arange(256)
wnd= fft.fftshift(0.54+0.46*np.cos(2*np.pi*n/(n.size-1)))
y= np.cos(0.86*t)**3
y= y*wnd
y[0]= 0
y= fft.fftshift(y)
Y = fft.fftshift(fft.fft(y))/256.0
w = np.linspace(-np.pi*fmax, np.pi*fmax, 257);w= w[:-1]
spectrum_plot(w,Y,r"Spectrum of $cos^3(0.86t) * w(t)$",magStyle='b-o',xLimit=[-4, 4])

#Question 3: Spectrum of cos(wo*t + d) & estimating 'wo' and 'd' from the spectrum
omega_o= 1; delta= np.pi/4          #assigning some values to omega and delta
t= np.linspace(-1*np.pi, 1*np.pi, 129);t=t[:-1]         #Spectrum of cos(wo*t + d) with Hamming window
dt= t[1]-t[0]; fmax= 1/dt
n= np.arange(128)
wnd= fft.fftshift(0.54+0.46*np.cos(2*np.pi*n/(n.size-1)))
y= np.cos(omega_o*t+ delta)*wnd 
y[0]= 0
y= fft.fftshift(y)
Y = fft.fftshift(fft.fft(y))/128.0
w = np.linspace(-np.pi*fmax, np.pi*fmax, 129);w= w[:-1]
spectrum_plot(w,Y,r"Spectrum of $cos(\omega_o t + \delta) * w(t)$",magStyle='b-o',xLimit=[-4, 4])

#Estimation of wo & d
wo_estim= np.sum(np.abs(Y)**2*np.abs(w))/(np.sum(abs(Y)**2))  #weighted mean to find wo      
i= np.abs(w-wo_estim).argmin()          #index where 'w' is closest to estimated 'wo' 
d_estim= np.angle(Y[i])         #phase at the index i gives estimated d
print("Question 3: \nThe estimated value of wo is:",wo_estim)           #printing estimated values
print("The original value of wo is:",omega_o)
print("The estimated value of delta is:",d_estim)
print("The original value of delta is:",delta)

#Question 4:Spectrum of cos(wo*t + d) & estimating 'wo' and 'd' from the spectrum, when noise is added
t= np.linspace(-1*np.pi, 1*np.pi, 129);t=t[:-1]
dt= t[1]-t[0]; fmax= 1/dt
n= np.arange(128)
wnd= fft.fftshift(0.54+0.46*np.cos(2*np.pi*n/(n.size-1)))
func= np.cos(omega_o*t+ delta)+ 0.1*np.random.randn(128)        #adding white gaussian noise
y= func.copy() *wnd
y[0]= 0
y= fft.fftshift(y)
Y = fft.fftshift(fft.fft(y))/128.0
w = np.linspace(-np.pi*fmax, np.pi*fmax, 129);w= w[:-1]
spectrum_plot(w,Y,r"Spectrum of $cos(\omega_o t + \delta) * w(t)$ with noise",magStyle='b-o',xLimit=[-4, 4])

wo_estim= np.sum((np.abs(Y)**2*np.abs(w))/(np.sum(abs(Y)**2)))      #estimating and printing the values
i= np.abs(w-wo_estim).argmin()
d_estim= np.angle(Y[i])
print("Question 4: \nThe estimated value of wo for noisy signal is:",wo_estim)
print("The estimated value of delta for noisy signal is:",d_estim)

#Question 5:Spectrum of cos(16*t*(1.5+(t/2*pi)))..(Chirped Signal)
t= np.linspace(-1*np.pi, 1*np.pi, 1025);t=t[:-1]      #Spectrum of cos(16*t*(1.5+(t/2*pi))) with Hamming window  
dt= t[1]-t[0]; fmax= 1/dt
n= np.arange(1024)
wnd= fft.fftshift(0.54+0.46*np.cos(2*np.pi*n/(n.size-1)))
y= np.cos(16*t*(1.5+(t/(2*np.pi))))
y= y*wnd
y[0]= 0
Y = fft.fftshift(fft.fft(y))/1024.0
w = np.linspace(-np.pi*fmax, np.pi*fmax, 1025);w= w[:-1]
spectrum_plot(w,Y,r"DFT of $cos(16(1.5 + \frac{t}{2\pi})t) *w(t)$ ",magStyle='b-',phaseStyle='r.-',xLimit=[-64, 64])

#Question 6: Variation of frequency of the above signal with time.
y_piece = np.split(y, 1024//64)         #breaking the signal into pieces
X = np.zeros((1024//64, 64), dtype=complex)     
for i in range(1024//64):           #Finding DFT for the split signal
    X[i] = fft.fftshift(fft.fft(y_piece[i]))/64

t = t[::64]     #Surface plot of the 2D array containing the DFT of each piece
w = np.linspace(-fmax*np.pi, fmax*np.pi, 65);w=w[:-1]
t, w = np.meshgrid(t, w)
fig = plt.figure(fig_no)
ax = fig.add_subplot(111, projection='3d')
surface = ax.plot_surface(w, t, abs(X).T, cmap='jet')
fig.colorbar(surface)
plt.xlabel(r"Frequency $\to$")
plt.ylabel(r"Time $\to$")
plt.title(r"Magnitude $\|Y\|$")
plt.show()