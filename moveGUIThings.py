import os.path as pth
import numpy as np

def moveThings(startPoint,shift,inPath,outPath):
    fileSize = pth.getsize(inPath)

    fid    = open(inPath,'rb')
    fidout = open(outPath,'wb')

    while (fid.tell() < fileSize):
        x = myReadLine(fid)

        i = x.find('top="')
        while (i != -1):
            i2 = x.find('"',i+5)
            topNum = int(x[(i+5):i2])

            if (topNum > startPoint):
                x = x[:(i+5)]+str(topNum+shift)+x[i2:]

            i = x.find('top="',i+5)

        fidout.write(x.encode('utf-8')+b'\r\n')

    fid.close()
    fidout.close()


def myReadLine(fid):
    xOut = b''

    x = fid.read(1)
    while (x!=b'' and x!=b'\r' and x!=b'\n'):
        xOut = xOut + x
        x = fid.read(1)

    if (x==b'\r'):
        x = fid.read(1)
        if (x!=b'' and x!=b'\n'):
            fid.seek(-1,1)

    xOut = xOut.decode('utf-8')
    return xOut
