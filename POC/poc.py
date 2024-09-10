
effectChars = ["*", "#", ">", "=", "-"]

def loadFile(path):
    f = open(path, "r")
    return f.read()

def Lexer(toParse):
    global effectChars

    o = []
    buffer = ""

    breakingChars = ["\n"]

    for i in range(len(toParse)):
        if toParse[i] in breakingChars:
            o += [buffer]
            buffer = ""
        elif toParse[i] in effectChars:
            o += [buffer, toParse[i]]
            buffer = ""
        else:
            buffer += toParse[i]
        
        for i in range(len(o)):
            if o[len(o)-i-1] == "":
                o.pop(len(o)-i-1)
    return o

def Walker(lexed):
    global effectChars
    o = []
    #headers [1 - 5], list element, numbered list element, bold, italic, highlights
    #        0      1     2     3     4     5     6     7      8       9      10
    efx = ["none" ,"h1", "h2", "h3", "h4", "h5", "le", "ble", "bold", "ita", "hglt"]
    current = 0
    for i in range(len(lexed)):
        #check if lexed is a spec char 
        if lexed[i] in effectChars:
            #TODO
            if lexed[i] == "#":
                if  current < 5:
                    current+=1
            if lexed[i] == "*":

                if current == 9 and lexed[i+1] == "*":
                    current = 8

                if current == 0:
                    current = 9

        else:
            if current == 0:
                o += [(lexed[i], efx[current])]
            elif current >=1 and current < 6:
                o += [(lexed[i], efx[current])]
            current = 0

    return o

print(
    Walker(
        Lexer(
            loadFile("POC\Sample.md")
        )
    )
)
