import numpy as np

'''
 reptabs(inPath,outPath) copies the source code in 'inPath'
 and writes it to 'outPath' with tabs replaced with four spaces
'''
def reptabs(inPath,outPath):
    BLOCK_SIZE = 512
    iLow       = 0
    iHigh      = 0

    fid    = open(inPath,'rb')
    fidout = open(outPath,'wb')

    x = np.fromfile(fid,np.uint8,BLOCK_SIZE)
    while (x.size > 0):
        nTabs = np.sum(x==9)

        if (nTabs == 0):
            fidout.write(x.tobytes())
            x = np.fromfile(fid,np.uint8,BLOCK_SIZE)
            continue

        xout = np.zeros((x.size+3*nTabs,),dtype=np.uint8)

        iLow  = 0
        iHigh = 0
        iOut  = 0
        for iTab in range(nTabs):
            iHigh += np.argmax(x[iHigh:]==9)

            xout[iOut:(iOut+iHigh-iLow)] = x[iLow:iHigh]
            iOut += iHigh-iLow

            xout[iOut:(iOut+4)] = 32
            iOut += 4

            iHigh = iHigh+1
            iLow  = iHigh

        if (iOut < xout.size):
            xout[iOut:] = x[iLow:]

        fidout.write(xout.tobytes())
        x = np.fromfile(fid, np.uint8, BLOCK_SIZE)

    fid.close()
    fidout.close()
