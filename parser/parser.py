import re
import parser.lexer as pl

class Rule:
    start = ""
    end = ""
    tag = ""
    justText = False 
    canBeNested = False 
    previousChar = ""

    def __init__(self, tg, st, end="", justText = False, canBeNested = False, prevChar = ""):
        self.tag = tg 
        self.start = st 
        self.end = end 
        self.justText = justText
        self.canBeNested = canBeNested
        self.previousChar = prevChar 

table_regex = re.compile(r"((\|\s([^\n])+)\n)+\n",re.MULTILINE)
#       tag   1st c   last c onlyText nested lastChar 
rules = [
    Rule("h1",   "#",     "\n" , True),
    Rule("h2",   "##",    "\n" , True),
    Rule("h3",   "###",   "\n" , True),
    Rule("h4",   "####",  "\n" , True),
    Rule("h5",   "#####", "\n" , True),
    Rule("*" ,   "*",     "*") ,
    Rule("*" ,   "_",     "_") ,
    Rule("**",   "**",    "**"),
    Rule("**",   "__",    "__"),
    Rule("==",   "==",    "==" , True),
    Rule("~~",   "~~",    "~~"),
    Rule("$$",   "$$",    "$$" , True),
    Rule("$",    "$",     "$"  , True),
    Rule("()",   "(",     ")"  , False, True),
    Rule("[]" ,  "[",     "]"  , True),
    Rule("[[]]", "[[",    "]]" , True),
    Rule("![[]]","![[",   "]]" , True),
    Rule("![",   "![",    "]"  , True),
    Rule("```",  "```",   "```", True),
    Rule("-",    "-",     "\n" , False, False, "\n"),
    Rule("-_",   "-",     "\n",  False, False, "\t"),
    Rule("-_",   "-",     "\n",  False, False, "    "),
    Rule(">",    ">",     "\n",  False, False),
    Rule("---",  "---",   "\n"),
    Rule("^",    "^",     "\n"),
]

class Node:
    #tag = ""
    #children = []

    def __init__(self,t = "", c = []):
        self.tag = t
        self.children = c.copy()
        self.value = ""

    def addChildren(self, cln, prev="¤"):
        global rules 
        global table_regex        
        nlist = cln.copy()
        
        if nlist == []:
            return []

        if re.search(table_regex ,nlist[0]) != None:
            table_node = parse_table_block(nlist[0])
            self.children += [table_node]
            return self.addChildren(nlist[1:], prev=nlist[0][-1])

        idx = -1 #rule index 
        noffset = 1 #number of elements to remove before next operation
        #check if any rules work 
        for i in range(len(rules)):
            if nlist[0] == rules[i].start:
                if rules[i].previousChar != "":
                    #print(nlist[0], repr(prev))
                    if rules[i].previousChar == prev:
                        idx = i
                        break 
                else:
                    idx = i
                    break 
        #print(nlist[0])
        if idx < 0:
            #no rules where met 
            if nlist[0] != "\n":
                self.children += [nlist[0]]
            else:
                self.children += [Node("br", [""])]
            return self.addChildren(nlist[1:], prev=nlist[0])
        
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
                if len(nlist) == 1:
                    buffer = nlist 
                else:
                    while nlist[off] != r.end:
                        buffer += nlist[off] 
                        off += 1
                        if off >= len(nlist):
                            break
                nNode.children = [buffer]
                noffset = off+1
        else:
            if r.end == "":
                print("You should not be there : 75")
                nNode.addChildren([nlist[1]], nlist[1][-1])
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
                if r.canBeNested:
                    nNode.children += buffer 
                else: 
                    nNode.addChildren(buffer)
                noffset = off+1 

        self.children += [nNode]
        previous = ""
        try:
            previous =  nlist[noffset-1][-1]
        except:
            #print("Error occured :", nlist[noffset:])
            previous = ""
        return self.addChildren(nlist[noffset:], previous)

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
        if tree.children[idx].tag == "-" or tree.children[idx].tag == "-_":
            buffer = []
            offset = 0
            t = lambda x : \
                ( type(tree.children[x]) == Node ) and \
                ( tree.children[x].tag == "-" or tree.children[x].tag == "-_")
            
            while t(idx - offset):
                buffer += [Node("le",tree.children[idx - offset].children)]
                offset += 1
                if idx - offset < 0:
                    break
            nNode = Node("ls", buffer)
            tree.children[idx-offset+1:idx+1] = []
            tree.children.insert(idx-offset+1, nNode)
            continue
        #numbered lists :
        numerals =  [str(i) + "." for i in range(10)]
        if tree.children[idx].tag in numerals:
            buffer = []
            offset = 0
            
            while type(tree.children[idx-offset]) == Node and \
                tree.children[idx-offset].tag in numerals: 
 
                buffer += [Node("ne", tree.children[idx - offset].children)]
                offset += 1
                if idx - offset < 0:
                    break 
            nNode = Node("nl", buffer)
            tree.children[idx-offset+1:idx+1] = []
            tree.children.insert(idx-offset+1, nNode)
            continue
        # adds a weird nesting that needs to be fixed, but not right now. -(le(le; le; le,))
    
        #Web/external links
        if tree.children[idx].tag == "()":
            if type(tree.children[idx-1]) == Node:
                if tree.children[idx-1].tag == "[]":
                    nNode = Node("wl") #Web Link 
                    nNode.children = ["".join(tree.children[idx].children)
                                      , tree.children[idx-1].children[0]]
                    tree.children[idx-1:idx+1] = []
                    tree.children.insert(idx-1, nNode) 
                    continue
           
            ch = tree.children[idx].children[:]
            tree.children[idx].children = []
            tree.children[idx].addChildren(ch)
            newList = ["("] + tree.children[idx].children + [")"]
            tree.children.pop(idx)
            for j in range(len(newList)):
                tree.children.insert(idx + j, newList[j])
            
    
    TreeShaker(tree, depth-1)
    return tree
#this function was made by chatgpt, i apologize... I will rewrite later, but rn i just want it to go in prod 
def parse_table_block(table_block):
    lines = table_block.strip().split('\n') 
    
    # Create the root node for the table 
    table_node = Node('table')
    # Create and populate the thead (header)
    thead_node = Node('thead')
    header_row = Node('tr')
    
    headers = [header.strip() for header in lines[0][1:-1].split('|')]
    alignments = [alignment.strip() for alignment in lines[1][1:-1].split('|')]
    
    for header, alignment in zip(headers, alignments):
        th_node = Node('th')
        th_node.addChildren(pl.Lexer(header)) 
        th_node.alignment = alignment  # Store alignment as an attribute 
        header_row.children += [th_node]
    
    thead_node.children += [header_row]
    table_node.children += [thead_node]
    # Create and populate the tbody (body)
    tbody_node = Node('tbody')
    
    for row in lines[2:]:
        tr_node = Node('tr')
        cells = [cell.strip() for cell in row[1:-1].split('|')]
        for i, cell in enumerate(cells):
            td_node = Node('td')
            td_node.addChildren(pl.Lexer(cell)) 
            td_node.alignment = alignments[i]  # Store alignment as an attribute 
            tr_node.children += [td_node]
        tbody_node.children += [tr_node]
    
    table_node.children += [tbody_node]
    return table_node

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


