import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img

def plotSpectrogram(x,Fs,win,noverlap,nfft,clims=None,axs=None):
    f,t,Sxx = sig.spectrogram(x,Fs,win,len(win),noverlap,nfft,None,mode='magnitude')

    myAxs    = axs if (axs != None) else plt.gca()
    imHandle = myAxs.imshow(20*np.log10(Sxx[::-1,:]),cmap='jet',extent=[t[0],t[-1],f[0],f[-1]],interpolation=None,aspect='auto')

    if (clims != None):
        imHandle.set_clim(clims)

    if (axs == None):
        return myAxs

def setClim(clims):
    ax = plt.gca()

    try:
        ax = next(x for x in ax.get_children() if isinstance(x,img.AxesImage))
        ax.set_clim(clims)
    except StopIteration:
        pass
    except:
        raise

def showHist(nbins):
    ax = plt.gca()
    try:
        ax = next(x for x in ax.get_children() if isinstance(x,img.AxesImage))
    except StopIteration:
        return

    I = ax.get_array()
    I = I.reshape((I.size,))

    plt.figure()
    ax = plt.hist(I,nbins)
