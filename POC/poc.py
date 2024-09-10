
effectChars = ["*", "#", ">", "=", "-", "_", "~", "\\", "\n"]

efx = ["#", "##", "###", "####", "#####", "*", "**", "_", "__", "-", "---", "=="]

class Node:
    tag = ""
    value = ""
    children = []
    
    def __init__(self, t="", c=[]):
        self.tag = t 
        self.children = c.copy()

    def addChildren(self, cln):
        global efx 
        if cln is None:
            return []
        if len(cln) == 0:
            return []
        nlist = cln.copy()

        #not nested first 
        if nlist[0] in efx[:5]:
            nNode = Node(nlist[0], [nlist[1]])
            self.children += [nNode]
            self.addChildren(nlist[2:])

        elif nlist[0] == "\n":
            nNode = Node("bl", [""])
            self.children += [nNode]
            self.addChildren(nlist[1:])
        
        elif nlist[0] == "\n\n":
            nNode = Node("bbl", [""])
            self.children += [nNode]
            self.addChildren(nlist[1:])

        elif nlist[0] == "---":
            nNode = Node("---", [""])
            self.children += [nNode]
            self.addChildren(nlist[1:])

        #nested 
        elif nlist[0] == "*":
            if self.tag != "*":
                nNode = Node("*")
                nlist = nNode.addChildren(nlist[1:])
                self.children += [nNode]

                self.addChildren(nlist)
            else:
                print("second star")
                return nlist[1:]
        
        elif nlist[0] == "**":
            if self.tag != "**":
                nNode = Node("**")
                nlist = nNode.addChildren(nlist[1:])
                self.children += [nNode]
                
                self.addChildren(nlist)
            else:
                return nlist[1:]

        else:
            self.children += [nlist[0]]
            a = self.addChildren(nlist[1:])
            return a
        

        


def loadFile(path):
    f = open(path, "r")
    return f.read()

def Lexer(toParse):
    global effectChars

    o = []
    buffer = ""

    for i in range(len(toParse)):
        if toParse[i] in effectChars:
            o += [buffer, toParse[i]]
            buffer = ""
        else:
            buffer += toParse[i]
        
    return o

def Cleanup(lexed):
    o = []
    buf = ""
    l = len(lexed)
    for i in range(l):
        if lexed[l-i-1] == "":
            lexed.pop(l-i-1)
    for i in range(len(lexed)):
        if lexed[i] in effectChars:
            if buf == "":
                buf += lexed[i]
                continue
            if lexed[i] == buf[-1]:
                buf += lexed[i] 
            else:
                o+=[buf]
                buf = lexed[i]
        else:
            if buf != "":
                o+=[buf]
                buf = ""
            o += [lexed[i]]

    return o

def TreeBuilder(cln):
    global effectChars 

    trunk = Node("page")
    trunk.addChildren(cln)

    return trunk

def printTree(n, depth = 0):
    d = "|" + "-" * depth
    s =   " " * depth
    print(d + n.tag)
    for i in range(len(n.children)):
        if type(n.children[i]) == Node:
            printTree(n.children[i], depth+1)
        else:
            print("|" + s + "|-" + n.children[i])

lf = loadFile("POC/test.md")
l = Lexer(lf)
c = Cleanup(l)
w = TreeBuilder(c)


#print(l)
#print(c)
print("------------")
printTree(w)

