import os
import os.path as pth

def dircontents(dirPath):
    #
    # Input integrity check
    #
    if (not pth.isdir(dirPath)):
        return ([],[])

    dirPath_ = pth._getfullpathname(dirPath)
    if (dirPath_[-1] != '\\'):
        dirPath_ += '\\'

    #
    # Action
    #
    DirsList  = []
    FilesList = []
    FullList  = os.listdir(dirPath_)
    for currItem in FullList:
        currPath = dirPath_ + currItem
        if pth.isdir(currPath):
            DirsList.append(currPath+'\\')
        else:
            FilesList.append(currPath)

    return (DirsList,FilesList)


def deepdirslist(dirPath):
    #
    # Input integrity check
    #
    if (not pth.isdir(dirPath)):
        return []

    dirPath_ = pth._getfullpathname(dirPath)
    if (dirPath_[-1] != '\\'):
        dirPath_ += '\\'

    #
    # Action
    #
    DirsList,_ = dircontents(dirPath)
    if (len(DirsList) != 0):
        SubDirsList = []
        for subDir in DirsList:
            SubDirsList += deepdirslist(subDir)

        DirsList += SubDirsList

    return DirsList


def deepfileslist(*args):
    #
    # Input integrity check
    #
    if (len(args) == 0):
        return []

    dirPath = args[0]

    if (len(args) > 1):
        hasStr = args[1]

    if ( (len(args) == 1) or not isinstance(hasStr,str) ):
        hasStr = ''

    if (not pth.isdir(dirPath)):
        return []

    dirPath_ = pth._getfullpathname(dirPath)
    if (dirPath_[-1] != '\\'):
        dirPath_ += '\\'

    #
    # Action
    #
    DirsList,FilesList = dircontents(dirPath_)
    if (hasStr != ''):
        i = 0
        while (i < len(FilesList)):
            if (FilesList[i].find(hasStr) == -1):
                FilesList.__delitem__(i)
                continue

            i += 1

    if (len(DirsList) != 0):
        SubFilesList = []
        for subDir in DirsList:
            SubFilesList += deepfileslist(subDir,hasStr)

        FilesList += SubFilesList

    return FilesList


def dirdiff(pathA,pathB):
    #
    # Input integrity check
    #
    if ( (not pth.isdir(pathA)) or (not pth.isdir(pathB)) ):
        return -1

    pathA_ = pth._getfullpathname(pathA)
    if (pathA_[-1] != '\\'):
        pathA_ += '\\'

    pathB_ = pth._getfullpathname(pathB)
    if (pathB_[-1] != '\\'):
        pathB_ += '\\'

    diffCount = 0

    DirsA,FilesA = dircontents(pathA_)
    DirsB,FilesB = dircontents(pathB_)

    FilesDiff  = list(set(FilesA).difference(FilesB))
    diffCount += len(FilesDiff)

    if (len(FilesDiff) > 0):
        for fileName in FilesDiff:
            print(pth._getfullpathname())