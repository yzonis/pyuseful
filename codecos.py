import numpy as np

BLOCK_SIZE = 512

def pullsemicolon(inPath,outPath):
    fid    = open(inPath,'r')
    fidout = open(outPath,'w')

    x = fid.readline()
    while (len(x) > 0):
        ind_sc = x.rfind(';')
        nTabs = np.sum(x==TAB_ORD)

        if (nTabs == 0):
            fidout.write(x.tobytes())
            x = np.fromfile(fid,np.uint8,BLOCK_SIZE)
            continue

        xout = np.zeros((x.size+3*nTabs,),dtype=np.uint8)

        iLow  = 0
        iHigh = 0
        iOut  = 0
        for iTab in range(nTabs):
            iHigh += np.argmax(x[iHigh:]==TAB_ORD)

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


'''
 reptabs(inPath,outPath) copies the source code in 'inPath'
 and writes it to 'outPath' with tabs replaced with four spaces
'''
def reptabs(inPath,outPath):
    TAB_ORD = ord('\t')
    iLow    = 0
    iHigh   = 0

    fid    = open(inPath,'rb')
    fidout = open(outPath,'wb')

    x = np.fromfile(fid,np.uint8,BLOCK_SIZE)
    while (x.size > 0):
        nTabs = np.sum(x==TAB_ORD)

        if (nTabs == 0):
            fidout.write(x.tobytes())
            x = np.fromfile(fid,np.uint8,BLOCK_SIZE)
            continue

        xout = np.zeros((x.size+3*nTabs,),dtype=np.uint8)

        iLow  = 0
        iHigh = 0
        iOut  = 0
        for iTab in range(nTabs):
            iHigh += np.argmax(x[iHigh:]==TAB_ORD)

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
