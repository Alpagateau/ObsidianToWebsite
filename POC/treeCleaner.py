import poc 

def TreeShaker(tree):
    # The goal of this method is to read the tree and group branches together in a way that makes more sens.
    # It's in a way, a second parsing pass 
    
    if type(tree) != poc.Node:
        return 
    l = len(tree.children)
    for i in range(l):
        idx = l - i - 1 #use backward index to prevent out of bounds errors 
        
        #because of weird deletion thingies, need to recheck the boundaries 
        if idx >= len(tree.children):
            print("Out of bound area")
            continue

        #ofc, check if string  
        if type(tree.children[idx]) != poc.Node:
            continue 
        
        #lists
        if tree.children[idx].tag == "-":
            buffer = []
            offset = 0

            while type(tree.children[idx - offset]) == poc.Node and tree.children[idx - offset].tag == "-":
                buffer += [poc.Node("le",tree.children[idx - offset].children)]
                offset += 1
                if idx - offset < 0:
                    break
            nNode = poc.Node("ls", buffer)
            tree.children[idx-offset+1:idx+1] = []
            tree.children.insert(idx-offset+1, nNode)
            continue
        # adds a weird nesting that needs to be fixed, but not right now. -(le(le; le; le,))
    
        #Web/external links
        if tree.children[idx].tag == "()":
            if type(tree.children[idx-1]) != poc.Node:
                continue
            if tree.children[idx-1].tag == "[]":
                nNode = poc.Node("wl") #Web Link 
                nNode.children = [ tree.children[idx].children[0], tree.children[idx-1].children[0]]
                tree.children[idx-1:idx+1] = []
                tree.children.insert(idx-1, nNode) 
            continue

    return tree

"""
poc.printTree(
    TreeShaker(
        poc.TreeBuilder(
            poc.Cleanup(
                poc.Lexer(
                    poc.loadFile("POC/test.md")
                )
            )
        )
    )
)
"""

