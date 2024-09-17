import re
#list of characters used by the lexer to separate the text into tokens  
cutChars = [".", "`", "*",  "#", 
            "-", ">", "=",  "-", 
            "_", "~", "\\", "\n", 
            "$", "[", "]",  "(", ")",
            ] + [i for i in range(10)] 

#list of special tokens that will be built by the cleanup fonction 
tokens =[
    "#", "##", "###", "####", "#####", 
    "*", "**", "_", "__", "- ", "--", 
    "---", "==", "[", "[[", "]]", "]", 
    "$$", "$", "`", "```", "\\*", 
    "1.", "2.", "3.", "5.", "6.", "7.",
    "7.", "8.", "9."]

table_regex_ = re.compile(r'''

            ^\|(?:[^\|\n]*\|)+\s*\n              # Header row

                ^\|(?:[-:]+\|)+\s*\n                # Alignment row

                (?:^\|(?:[^\|\n]*\|)+\s*)+          # Data rows

            ''', re.VERBOSE | re.MULTILINE | re.DOTALL)

# Define the regex pattern

table_regex = r"((\|\s([^\n])+)\n)+\n"

opts = (re.MULTILINE | re.DOTALL)
#clean up lexed list by tokenizing it 
def Cleanup(cln):
    global tokens, table_regex, opts 
    lexed = cln.copy()
    if lexed == []:
        return []
    #print(lexed[0])
    if re.search(table_regex,lexed[0]) != None:
        return [lexed[0]] + Cleanup(lexed[1:])
    if lexed[0] in cutChars: 
        possibleTokens = [] 
        for t in range(len(tokens)):
            if "".join(lexed[:6]).find(tokens[t]) == 0:
               possibleTokens += [t] 
        
        if len(possibleTokens) == 0:
            return [lexed[0]]+Cleanup(lexed[1:])
        tkn = -1
        l = 0
        #print(lexed[0], [tokens[i] for i in possibleTokens])
        for i in range(len(possibleTokens)):
            if len(tokens[possibleTokens[i]]) > l:
                l = len(tokens[possibleTokens[i]])
                tkn = possibleTokens[i]
        #print("TOKEN : " + tokens[tkn])
        #print("len TOKEN : " + str(len(tokens[tkn])))
        #print(tkn, tokens[tkn],  len(lexed[len(tokens[tkn]):]))
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

    for matchNum, match in enumerate(ls, start=1):
        print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, 
                                                                            start = match.start(), 
                                                                            end = match.end(), 
                                                                            match = match.group()))
        offset = len("".join(toParse[:-1])) 
        ln = (match.end() - match.start())
        #print(offset, type(match.group()))
        print(toParse[-1][0:match.start() - offset])
        toParse = toParse[:-1] + [ toParse[-1][0:match.start()-offset], match.group(), toParse[-1][match.end()-offset:]]
    
    print(len(toParse))
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
        
    return Cleanup(o)


