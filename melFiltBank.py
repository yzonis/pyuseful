import numpy as np

def melFiltBank(nfft,Fs,nmels):
    freqLow  = 0
    freqHigh = 2595 * np.log10(1 + (Fs/2)/700)

    melVec = np.linspace(freqLow,freqHigh,nmels+2)
    hzVec  = 700 * (10**(melVec/2595) - 1)
    indVec = np.int16(np.round(hzVec / (Fs/nfft)))

    M = np.zeros((nmels,int(nfft/2+1)),dtype=np.double)
    for iFilt in range(nmels):
        iLeft    = indVec[iFilt]
        iMid     = indVec[iFilt+1]
        iRight   = indVec[iFilt+2]
        vecLeft  = np.arange(iLeft+1,iMid)
        vecRight = np.arange(iMid,iRight)

        M[iFilt,(iLeft+1):iMid]  = (vecLeft-iLeft)/(iMid-iLeft)
        M[iFilt,iMid:iRight] = (iRight-vecRight)/(iRight-iMid)

    melVec = melVec[1:-1]

    return (melVec,M)
