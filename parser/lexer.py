import re
#list of characters used by the lexer to separate the text into tokens  
cutChars = [".", "`", "*",  "#", 
            "-", ">", "=",  "-", 
            "_", "~", "\\", "\n", 
            "$", "[", "]",  "(", ")",
            "!", "^"] + [i for i in range(10)] 

#list of special tokens that will be built by the cleanup fonction 
tokens =[
    "#", "##", "###", "####", "#####", 
    "*", "**", "_", "__", "-", "--", "---", 
    "==", "[", "[[", "]]", "]", "![[", "[ ]", "[x]",
    "$$", "$", "`", "```", "\\*", 
    "1.", "2.", "3.", "5.", "6.", "7.",
    "7.", "8.", "9."]

# Define the regex pattern
old_table_regex = r"((\|\s([^\n])+)\n)+\n"
table_regex = r"((\|[^\n]+\|)\n)+"
opts = (re.MULTILINE | re.DOTALL)

#clean up lexed list by tokenizing it 
def Cleanup(cln):
    global tokens, table_regex, opts 
    threshold = 1000
     
    #prevent recursion overflow
    if len(cln) > threshold: 
        cidx = len(cln)//2
        while cln[cidx] in cutChars:
            cidx -= 1
        return Cleanup(cln[:cidx]) + Cleanup(cln[cidx:])

    lexed = cln.copy()
    if lexed == []:
        return []
    if re.search(table_regex,lexed[0]) != None:
        return [lexed[0]] + Cleanup(lexed[1:])
    if lexed[0] in cutChars: 
        possibleTokens = [] 
        for t in range(len(tokens)):
            if "".join(lexed[:9]).find(tokens[t]) == 0:
               possibleTokens += [t]  
        if len(possibleTokens) == 0:
            return [lexed[0]]+Cleanup(lexed[1:])
        tkn = -1
        l = 0
        for i in range(len(possibleTokens)):
            if len(tokens[possibleTokens[i]]) > l:
                l = len(tokens[possibleTokens[i]])
                tkn = possibleTokens[i]
        return [tokens[tkn]] + Cleanup(lexed[len(tokens[tkn]):])
    else:
        return [lexed[0]] + Cleanup(lexed[1:])

def Lexer(inputFile):
    global cutChars, table_regex, opts 
    
    
    o = []
    buffer = u""
    toParse = [inputFile]
    tables = []
    ls = re.finditer(table_regex, inputFile, re.MULTILINE)
    if len(inputFile) < 100:
        print("lexer", inputFile)

    for matchNum, match in enumerate(ls, start=1):
        
        #print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, 
        #                                                                    start = match.start(), 
        #                                                                    end = match.end(), 
        #                                                                    match = match.group()))
        if len(inputFile)<100:
            print(matchNum)
        offset = len("".join(toParse[:-1])) 
        ln = (match.end() - match.start())
        #print(offset, type(match.group()))
        #print(toParse[-1][0:match.start() - offset])
        toParse = toParse[:-1] + [ 
            toParse[-1][0:match.start()-offset],
            match.group(),
            toParse[-1][match.end()-offset:]]
     
    for i in range(len(toParse)):
        if re.search(table_regex, toParse[i]) != None:
            o += [toParse[i]]
            continue 
        for j in range(len(toParse[i])):
            if toParse[i][j] in cutChars:
                if buffer != "":
                    o += [buffer, toParse[i][j]]
                else:
                    o += [toParse[i][j]]
                buffer = u""
            else:
                buffer += toParse[i][j]    
        o+=[buffer]
    return Cleanup(o)


