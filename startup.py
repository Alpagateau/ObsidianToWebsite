import os 

filelistPath = "./Cache/filelist.txt"

def UpdateFileList():
    global filelistPath
    allFiles =  [i + ",Revisions/" + i for i in os.listdir("Revisions/")]
    allFiles += [i + ",Revisions/Cours/"+i for i in os.listdir("Revisions/Cours/")]
    allFiles += [i + ",Revisions/Preuves/"+i for i in os.listdir("Revisions/Preuves/")]
    
    if os.path.exists(filelistPath):
        os.remove(filelistPath) 

    f = open(filelistPath, "w")
    f.write([i+"\n" for i in allFiles])
