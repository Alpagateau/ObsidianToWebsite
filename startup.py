import os 

filelistPath = "./Cache/filelist.txt"

def UpdateFileList():
    global filelistPath
    allFiles =  [i + "," + i for i in os.listdir("Revisions/")]
    allFiles += [i + ",Cours/"+i for i in os.listdir("Revisions/Cours/")]
    allFiles += [i + ",Preuves/"+i for i in os.listdir("Revisions/Preuves/")]
    
    trueFiles = []
    for i in range(len(allFiles)):
        if ".md" in allFiles[i]:
            trueFiles += [allFiles[i]]

    if os.path.exists(filelistPath):
        os.remove(filelistPath) 

    f = open(filelistPath, "w", encoding="utf-8")
    f.write("".join([i+"\n" for i in trueFiles]))
