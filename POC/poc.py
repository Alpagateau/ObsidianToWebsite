
effectChars = ["`","*", "#", "-", ">", "=", "-", "_", "~", "\\", "\n", "$", "[", "]", "(", ")"] 

efx = ["#", "##", "###", "####", "#####", "*", "**", "_", "__", "-", "--", "---", "==", "[", "[[", "]", "]]", "$$", "$", "`", "```"]

class Node:
    tag = ""
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
            nNode = Node(nlist[0])
            buff = ""
            idx = 1
            while nlist[idx][0] != "\n":
                buff += nlist[idx]
                idx += 1
                if idx == len(nlist):
                    break
            nNode.children += [buff]
            self.children += [nNode]
            return self.addChildren(nlist[idx+1:])

        elif nlist[0] == "\n":
            nNode = Node("bl", [""])
            self.children += [nNode]
            return self.addChildren(nlist[1:])
        
        elif nlist[0] == "\n\n":
            nNode = Node("bbl", [""])
            self.children += [nNode]
            return self.addChildren(nlist[1:])

        elif nlist[0] == "---":
            nNode = Node("---", [""])
            self.children += [nNode]
            return self.addChildren(nlist[1:])

        elif nlist[0] == ">":
            nNode = Node(">", [nlist[1]])
            self.children += [nNode]
            return self.addChildren(nlist[2:])
        
        #Enclosed, when the first char is diff from the last char
        elif nlist[0] == "-":
            if nlist[1][0] == " ":
                nNode = Node("-")
                idx = 1
                temp = []
                while nlist[idx][0] != "\n":
                    if idx >= len(nlist):
                        break
                    temp += [nlist[idx]]
                    idx += 1
                    if idx == len(nlist):
                        break
                nNode.addChildren(temp)
                self.children += [nNode]
                if len(nlist) > len(temp)+1:
                    return self.addChildren(nlist[len(temp)+2:])
                else:
                    return self.addChildren(nlist[len(temp)+1:])
            else:
                self.children += [nlist[0] + nlist[1]]
                return self.addChildren(nlist[2:])
        
        elif nlist[0] == "[":
            nNode = Node("[]")
            idx = 1 
            temp = []
            while nlist[idx] != "]":
                if idx >= len(nlist):
                    break 
                temp += [nlist[idx]]
                idx+=1
                if idx == len(nlist):
                    break 
            nNode.children += [ "".join(temp) ] #Here, only concatenate 
            self.children += [nNode] 
            if len(nlist) > len(temp)+1:
                return self.addChildren(nlist[len(temp)+2:])
            else:
                return self.addChildren(nlist[len(temp)+1:])

        elif nlist[0] == "[[":
            nNode = Node("[[]]")
            idx = 1 
            temp = []
            while nlist[idx] != "]]":
                if idx >= len(nlist):
                    break 
                temp += [nlist[idx]]
                idx+=1
                if idx == len(nlist):
                    break 

            nNode.children += ["".join(temp)] #Here, only concatenate 
            self.children += [nNode] 
            if len(nlist) > len(temp)+1:
                return self.addChildren(nlist[len(temp)+2:])
            else:
                return self.addChildren(nlist[len(temp)+1:])
        
        elif nlist[0] == "(":
            nNode = Node("()")
            idx = 1 
            temp = []
            while nlist[idx] != ")":
                if idx >= len(nlist):
                    break 
                temp += [nlist[idx]]
                idx+=1
                if idx == len(nlist):
                    break 
            nNode.children += ["".join( temp )] #Here, only concatenate 
            self.children += [nNode] 
            if len(nlist) > len(temp)+1:
                return self.addChildren(nlist[len(temp)+2:])
            else:
                return self.addChildren(nlist[len(temp)+1:])
 
        elif nlist[0] == "\\":
            nNode = Node("\\")
            nNode.children = [ nlist[1] ]
            return self.addChildren(nlist[2:])
        #nested 
        elif nlist[0] == "*":
            if self.tag != "*":
                nNode = Node("*")
                nlist = nNode.addChildren(nlist[1:])
                self.children += [nNode]

                return self.addChildren(nlist)
            else:
                return nlist[1:]
        
        elif nlist[0] == "**":
            if self.tag != "**":
                nNode = Node("**")
                nlist = nNode.addChildren(nlist[1:])
                self.children += [nNode]

                return self.addChildren(nlist)
            else:
                return nlist[1:]

        elif nlist[0] == "__":
            if self.tag != "__":
                nNode = Node("__")
                nlist = nNode.addChildren(nlist[1:])
                self.children += [nNode]
                 
                return self.addChildren(nlist)
            else:
                return nlist[1:]

        elif nlist[0] == "_":
            if self.tag != "_":
                nNode = Node("_")
                nlist = nNode.addChildren(nlist[1:])
                self.children += [nNode]
                 
                return self.addChildren(nlist)
            else:
                return nlist[1:]

        elif nlist[0] == "==":
            if self.tag != "==":
                nNode = Node("==")
                nlist = nNode.addChildren(nlist[1:])
                self.children += [nNode]
                 
                return self.addChildren(nlist)
            else:
                return nlist[1:]
        
        elif nlist[0] == "~~":
            if self.tag != "~~":
                nNode = Node("~~")
                nlist = nNode.addChildren(nlist[1:])
                self.children += [nNode]
                 
                return self.addChildren(nlist)
            else:
                return nlist[1:] 
        
        elif nlist[0] == "***":
            if self.tag != "***":
                nNode = Node("***")
                nlist = nNode.addChildren(nlist[1:])
                self.children += [nNode]

                return self.addChildren(nlist)
            else:
                return nlist[1:]
        
        #Math blocks and code blocks 
        elif nlist[0] == "$":
            nNode = Node("$")
            buff = ""
            idx = 1
            while nlist[idx] != "$":
                buff += nlist[idx] 
                idx += 1
                if idx >= len(nlist):
                    break
            nNode.children += [buff]
            self.children += [nNode]
            return self.addChildren(nlist[idx+1:])
                
         
        elif nlist[0] == "$$":
            nNode = Node("$$")
            buff = ""
            idx = 1
            while nlist[idx] != "$$":
                buff += nlist[idx] 
                idx += 1
                if idx >= len(nlist):
                    break
            nNode.children += [buff]
            self.children += [nNode]
            return self.addChildren(nlist[idx+1:])
        
        elif nlist[0] == "`":
            if self.tag != "`":
                nNode = Node("`")
                nlist = nNode.addChildren(nlist[1:])
                self.children += [nNode]

                return self.addChildren(nlist) 
            else:
                return nlist[1:]
        
        elif nlist[0] == "```":
            if self.tag != "```":
                nNode = Node("```")
                nlist = nNode.addChildren(nlist[1:])
                self.children += [nNode]

                return self.addChildren(nlist) 
            else:
                return nlist[1:]
        
        #Plain text 
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
    print("| " * (depth-1), end="")
    print("|->" + n.tag)
    for i in range(len(n.children)):
        if type(n.children[i]) == Node:
            printTree(n.children[i], depth+1)
        else:
            print(("| " * depth) + "|->\"" + n.children[i] + "\"")

lf = loadFile("RemarkablePOC/index.md")
l = Lexer(lf)
c = Cleanup(l)
w = TreeBuilder(c)


#print(l)
#print(c)
#print("------------")
#printTree(w)

