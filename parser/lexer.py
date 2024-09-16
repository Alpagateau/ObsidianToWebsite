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

table_regex = re.compile(r'''

            ^\|.*\|\s*\n                # Header row

                ^\|[-:| ]+\|\s*\n           # Alignment row

                (?:^\|.*\|\s*)+            # Data rows

            ''', re.VERBOSE | re.MULTILINE | re.DOTALL)
#clean up lexed list by tokenizing it 
def Cleanup(cln):
    global tokens 
    lexed = cln.copy()
    if lexed == []:
        return []
    #print(lexed[0])
    if table_regex.search(lexed[0]) != None:
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
    global cutChars
    o = []
    buffer = u""
    toParse = []
    notLs = re.split(table_regex ,inputFile)
    ls = re.findall(table_regex, inputFile)
    for i in range(len(ls)):
        toParse += [notLs[i], ls[i]]
    toParse += [notLs[-1]]
    for i in range(len(toParse)):
        if table_regex.search(toParse[i]) != None:
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


