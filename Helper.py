import os


def DirStr2List(dirStr: str):
    return list(map(str, dirStr.split(',')))


def DirList2FileNameList(dirList):
    filenames = []
    for dir in dirList:
        for root, dirs, files in os.walk(dir):
            for filename in files:
                os.chdir(root)
                filenames.append(os.path.join(os.getcwd(), filename))
    return filenames


def AddSuffixToFullFilename(filename, suffix):
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename).split(".")[0]
    extension = os.path.basename(filename).split(".")[1]
    return os.path.join(dirname, basename+suffix+"."+extension)
