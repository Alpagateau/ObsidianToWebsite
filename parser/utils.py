
IMAGE_EXT = ["apng", "gif", "ico", "cur", "jpg", "jpeg", "jfif", "pjpeg", "pjp", "png", "svg"]

def LoadFile(path):
    return open(path, "r", encoding="utf-8").read()

def LoadBinary(filename):
    with open(filename, 'rb') as file_handle:
        return file_handle.read()

def GetExtension(f):
    buff = ""
    for i in range(len(f)):
        if f[len(f) - i] == ".":
            return buff 
        buff = f[len(f) - i - 1] + buff 

def GetFileName(f):
    ext = ""
    passed = False 
    buff = ""
    if "." not in f:
        passed = True
    for i in range(len(f)):
        if not passed:
            if f[len(f) - i - 1] == ".":
                passed = True 
            else:
                ext = f[len(f) - i - 1] + ext 
        else:
            if f[len(f) - i - 1] == "/":
                return (buff, ext)
            else:
                buff = f[len(f) - i - 1] + buff
    return (buff, ext)

