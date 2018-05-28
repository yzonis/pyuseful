import os
import os.path as pth

def dircontents(dirPath):
    #
    # Input integrity check
    #
    dirPath_ = dirverify(dirPath)
    if (dirPath_ == ''):
        return ([],[])
    sep = dirPath_[-1]

    #
    # Action
    #
    DirsList  = []
    FilesList = []
    FullList  = os.listdir(dirPath_)
    for currItem in FullList:
        currPath = dirPath_ + currItem
        if pth.isdir(currPath):
            DirsList.append(currPath+sep)
        else:
            FilesList.append(currPath)

    return (DirsList,FilesList)


def deepdirslist(dirPath):
    DirsList,_ = dircontents(dirPath)
    if (DirsList.__len__() != 0):
        SubDirsList = []
        for subDir in DirsList:
            SubDirsList += deepdirslist(subDir)

        DirsList += SubDirsList

    return DirsList


def deepfileslist(*args):
    #
    # Input integrity check
    #
    if (args.__len__() == 0):
        return []

    dirPath = args[0]

    if (args.__len__() > 1):
        hasStr = args[1]

    if ( (args.__len__() == 1) or not isinstance(hasStr,str) ):
        hasStr = ''

    #
    # Action
    #
    DirsList,FilesList = dircontents(dirPath)
    if (hasStr.__len__() != 0):
        i = 0
        while (i < FilesList.__len__()):
            if (FilesList[i].find(hasStr) == -1):
                FilesList.__delitem__(i)
                i = i - 1

            i = i + 1

    if (DirsList.__len__() != 0):
        SubFilesList = []
        for subDir in DirsList:
            SubFilesList += deepfileslist(subDir,hasStr)

        FilesList += SubFilesList

    return FilesList


def dirverify(dirPath):
    '''
    verifies that the input string is a full-path to a directory

    input:
      dirPath - a string to be checked

    output:
      dirPath_ - an empty string in case the input string is not
                 a directory or a relative and not full path.
                 in case the input string is indeed a full-path,
                 the output is the full path with an additional 
                 dir separator ('\' or '/') in case there wasn't
                 one at the end of the input string
    '''

    if not pth.isdir(dirPath):
        return ''

    if ( (dirPath[0] == '.') or (dirPath[:2] == '..') ):
        return ''

    if (dirPath.find('/') != -1):
        sep = '/'
    elif (dirPath.find('\\') != -1):
        sep = '\\'

    dirPath_ = dirPath
    if (dirPath_[-1] != sep):
        dirPath_ += sep

    return dirPath_

A = deepfileslist('C:\\Users\\yaniv\\Desktop\\calibrationData\\evaluationChamber\\2017-09-27_sys1.3_damage_tests')