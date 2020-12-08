import numpy as np

def moveControls(filePath,xRange,yRange,xDiff,yDiff):
    fid = open(filePath,'r')

    rowStr = fid.readline()
    try:
        xTop, iTop1, iTop2          = extractField(rowStr, 'top')
        xLeft, iLeft1, iLeft2       = extractField(rowStr, 'left')
        xWidth, iWidth1, iWidth2    = extractField(rowStr, 'width')
        xHeight, iHeight1, iHeight2 = extractField(rowStr, 'height')
    except SyntaxError:
        pass
    except:
        raise

    locs1 = np.sort([iTop1,iLeft1,iWidth1,iHeight1])
    locs2 = np.sort([iTop2,iLeft2,iWidth2,iHeight2])

    newStr = rowStr[:locs1[0]] + str(xTop+yDiff[1]) +
             rowStr[(locs2[0]+1):locs1[1]]

def extractField(inStr, fieldName):
    ind = inStr.find(fieldName)
    if (ind == -1):
        raise SyntaxError('didn''t find field in string')

    iStart = inStr.find('\"', ind) + 1
    iEnd   = inStr.find('\"', iStart)

    return int(inStr[iStart:iEnd])
