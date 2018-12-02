import numpy as np

def batchExtract(pathList,extractFunc,outPath):
    '''
    batchExtract(pathList,extractFunc,outPath) assists in data analysis in cases where:

     - the data is stored in multiple files
     - an initial analysis is certainly needed on all the files and is done by running
       the same function on each of these files (e.g. welch spectral density estimation)
     - the user assumes she/he will probably want to return and review the
       results of this initial analysis with different ideas for further analysis, over
       and over again
     - the overall initial-analyses on all of the files takes very long

    In these cases, the user can use batchExtract() to make the initial analysis on all
    of the files ONCE, and then make this initial analysis results available and
    easily fetchable with a much shorter response time.

    :param pathList: The list of paths to the files, or alternatively, paths to
                     directories containing a bunch of files each
    :param extractFunc: A pointer to a function that performs the initial analysis
    :param outPath: A path to save all the initial analysis results to
    :return: a fail/success flag
    '''

    DOUBLE_PRECISION = False

    if (DOUBLE_PRECISION):
        bytesPerSample = 8
    else:
        bytesPerSample = 4

    ########
    # Action
    ########
    try:
        fid = open(outPath,'wb')
        for currPath in pathList:
            fid.write(b'\xaa\xaa\xbb\xbb'*2)

            dataDict = extractFunc(currPath)

            fid.write(np.uint16(len(dataDict['mainTtl'])).tobytes())
            fid.write(dataDict['mainTtl'].encode('utf-8'))

            for ttl,val in dataDict.items():
                if ( (ttl == 'mainTtl') or (ttl == 'subTitles') ):
                    continue

                if dataDict['subTitles']:
                    fid.write('subttl'.encode('utf-8'))
                    fid.write(np.uint16(len(ttl)).tobytes())
                    fid.write(ttl.encode('utf-8'))

                fid.write(np.uint16(len(val)*bytesPerSample).tobytes())
                if (DOUBLE_PRECISION):
                    fid.write(np.double(val).tobytes())
                else:
                    fid.write(np.float32(val).tobytes())

        return True
    except:
        try:
            fid.close()
        except NameError:
            pass
        except:
            raise

        return False
