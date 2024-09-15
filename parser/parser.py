class Rule:
    start = ""
    end = ""
    tag = ""
    justText = False 
    canBeNested = False 
    
    def __init__(self, tg, st, end="", justText = False, canBeNested = False):
        self.tag = tg 
        self.start = st 
        self.end = end 
        self.justText = justText
        self.canBeNested = canBeNested

rules = [
    Rule("h1",  "#",     "\n", True),
    Rule("h2",  "##",    "\n", True),
    Rule("h3",  "###",   "\n", True),
    Rule("h4",  "####",  "\n", True),
    Rule("h5",  "#####", "\n", True),
    Rule("*" ,  "*",     "*"),
    Rule("*" ,  "_",     "_"),
    Rule("**",  "**",    "**"),
    Rule("**",  "__",    "__"),
    Rule("==",  "==",    "==", True),
    Rule("~~",  "~~",    "~~"),
    Rule("$$",  "$$",    "$$", True),
    Rule("$ ",  "$",     "$",  True),
    Rule("()",  "(",     ")",  False, True),
    Rule("[]" , "[",     "]",  True),
    Rule("[[]]","[[",    "]]", True),
    Rule("```", "```",   "```",True),
    Rule("-",   "-",     "\n")
]

class Node:
    #tag = ""
    #children = []

    def __init__(self,t = "", c = []):
        self.tag = t
        self.children = c.copy()

    def addChildren(self, cln):
        global rules 
        
        nlist = cln.copy()
        
        if nlist == []:
            return []
        idx = -1 #rule index 
        noffset = 1 #number of elements to remove before next operation
        #check if any rules work 
        for i in range(len(rules)):
            if nlist[0] == rules[i].start:
                idx = i
                break 
        #print(nlist[0])
        if idx < 0:
            #no rules where met 
            self.children += [nlist[0]]
            return self.addChildren(nlist[1:])
        
        r = rules[idx]
        nNode = None
        nNode = Node(r.tag)
        if r.justText:
            #print(r.tag)
            if r.end == "":
                nNode.children = [nlist[1]]
            else:
                buffer = ""
                off = 1
                while nlist[off] != r.end:
                    buffer += nlist[off] 
                    off += 1
                    if off == len(nlist):
                        break
                nNode.children = [buffer]
                noffset = off+1
        else:
            if r.end == "":
                print("You should not be there : 75")
                nNode.addChildren([nlist[1]])
            else:
                buffer = []
                off = 1
                opened = 1
                while nlist[off] != r.end or opened != 1:
                    if r.canBeNested:
                        if nlist[off] == r.start:
                            opened += 1
                        if nlist[off] == r.end:
                            opened -= 1
                    buffer += [nlist[off]]
                    off += 1
                    if off == len(nlist):
                        break 
                #print(r.tag, " : ", buffer)
                if opened != 1:
                    print("PARSING ERROR : " + r.tag + " -> No matching " + r.end) 
                #print(r.tag + " : Buffer Lenght : " + str(len(buffer)))
                nNode.addChildren(buffer)
                noffset = off+1 

        self.children += [nNode]
        return self.addChildren(nlist[noffset:])

def TreeShaker(tree, depth=1):
    # The goal of this method is to read the tree and group branches together in a way that makes more sens.
    # It's in a way, a second parsing pass 
    if depth < 0:
        return
    if type(tree) != Node:
        return 
    l = len(tree.children)
    for i in range(l):
        idx = l - i - 1 #use backward index to prevent out of bounds errors 
        
        #because of weird deletion thingies, need to recheck the boundaries 
        if idx >= len(tree.children):
            print("Out of bound area")
            continue

        #ofc, check if string  
        if type(tree.children[idx]) != Node:
            continue 
        
        #lists
        if tree.children[idx].tag == "-":
            buffer = []
            offset = 0

            while type(tree.children[idx - offset]) == Node and tree.children[idx - offset].tag == "-":
                buffer += [Node("le",tree.children[idx - offset].children)]
                offset += 1
                if idx - offset < 0:
                    break
            nNode = Node("ls", buffer)
            tree.children[idx-offset+1:idx+1] = []
            tree.children.insert(idx-offset+1, nNode)
            continue
        # adds a weird nesting that needs to be fixed, but not right now. -(le(le; le; le,))
    
        #Web/external links
        if tree.children[idx].tag == "()":
            if type(tree.children[idx-1]) != Node:
                continue
            if tree.children[idx-1].tag == "[]":
                nNode = Node("wl") #Web Link 
                nNode.children = ["".join(tree.children[idx].children), tree.children[idx-1].children[0]]
                tree.children[idx-1:idx+1] = []
                tree.children.insert(idx-1, nNode) 
                continue
            newList = ["("] + tree.children[idx].children + [")"]
            tree.children.pop(idx)
            for j in range(len(newList)):
                tree.children.insert(idx + j, newList[j])
            
    
    TreeShaker(tree, depth-1)
    return tree



def BuildTree(lexed):
    tree = Node("page")
    tree.addChildren(lexed)
    return TreeShaker(tree)

def PrintTree(n, depth = 0):
    print("| " * (depth-1), end="")
    print("|->" + n.tag)
    if depth > 10:
        print("| " * (depth -1) + "Too deep")
        return
    for i in range(len(n.children)):
        if type(n.children[i]) == type(Node()):
            PrintTree(n.children[i], depth+1)
        else:
            if n.children[i] == "\n":
                print(("| " * depth) + "|->\"" + "\\n" + "\"")
            else:
                print(("| " * depth) + "|->\"" + n.children[i] + "\"")


