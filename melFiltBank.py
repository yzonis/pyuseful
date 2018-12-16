import numpy as np

def melFiltBank(nfft,Fs,nmels,normFlag):
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

        if (iLeft < iMid):
            vecLeft                 = np.arange(iLeft+1,iMid)
            M[iFilt,(iLeft+1):iMid] = (vecLeft-iLeft) / (iMid-iLeft)

        if (iMid < iRight):
            vecRight             = np.arange(iMid,iRight)
            M[iFilt,iMid:iRight] = (iRight-vecRight) / (iRight-iMid)
        else:
            M[iFilt,iMid] = 1

        if (normFlag):
            M[iFilt,:] /= hzVec[iFilt+2] - hzVec[iFilt]

    melVec = melVec[1:-1]

    return (melVec,M)
