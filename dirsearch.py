import os
import os.path as pth

def dircontents(dirPath,**kargs):
    #
    # Input integrity check
    #
    if ('fullpath' in kargs.keys()):
        fullpath = kargs['fullpath']
    else:
        fullpath = True

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

    if (fullpath):
        for currItem in FullList:
            currPath = dirPath_ + currItem
            if pth.isdir(currPath):
                DirsList.append(currPath)
            else:
                FilesList.append(currPath)
    else:
        for currItem in FullList:
            if pth.isdir(dirPath_ + currItem):
                DirsList.append(currItem)
            else:
                FilesList.append(currItem)

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
                FilesList.pop(i)
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

    #
    # Action
    #
    diffCount     = 0
    basepathStack = ['']
    while (len(basepathStack) != 0):
        basepath = basepathStack.pop(-1)

        DirsA,FilesA = dircontents(pathA_+basepath,fullpath=False)
        DirsB,FilesB = dircontents(pathB_+basepath,fullpath=False)

        FilesDiff  = list(set(FilesA).difference(FilesB)) + list(set(FilesB).difference(FilesA))
        diffCount += len(FilesDiff)

        if (len(FilesDiff) > 0):
            for fileName in FilesDiff:
                print('xf : '+basepath+fileName)

        DirsDiff   = list(set(DirsA).difference(DirsB)) + list(set(DirsB).difference(DirsA))
        diffCount += len(DirsDiff)

        if (len(DirsDiff) > 0):
            for dirName in DirsDiff:
                print('xd : '+basepath+dirName+'\\')

        FilesCommon = list(set(FilesA).intersection(FilesB))
        if (len(FilesCommon) != 0):
            for filename in FilesCommon:
                fid1 = open(pathA_+basepath+filename,'rb')
                fid2 = open(pathB_+basepath+filename,'rb')
                x1   = fid1.read(16384)
                x2   = fid2.read(16384)

                sameFlag = True
                while ((x1 != b'') and (x2 != b'')):
                    if (x1 != x2):
                        sameFlag = False
                        break

                    x1 = fid1.read(16384)
                    x2 = fid2.read(16384)

                fid1.close()
                fid2.close()

                if (not sameFlag):
                    diffCount += 1
                    print('!f : '+basepath+filename)

        DirsCommon = list(set(DirsA).intersection(DirsB))
        if (len(DirsCommon) != 0):
            for dirname in DirsCommon:
                basepathStack.append(basepath+dirname+'\\')

    print('\nTotal diffs: '+str(diffCount))

    return diffCount

def nofiles(dirPath):
    #
    # Input integrity check
    #
    if (not pth.isdir(dirPath)):
        return False

    dirPath_ = pth._getfullpathname(dirPath)
    if (dirPath_[-1] != '\\'):
        dirPath_ += '\\'

    #
    # Action
    #
    basepathStack = ['']
    while (len(basepathStack) != 0):
        basepath   = basepathStack.pop(-1)
        Dirs,Files = dircontents(dirPath_+basepath,fullpath=False)

        if (len(Files) != 0):
            return False

        if (len(Dirs) != 0):
            for dirname in Dirs:
                basepathStack.append(basepath+dirname+'\\')

    return True
