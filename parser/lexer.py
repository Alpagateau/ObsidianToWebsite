
#list of characters used by the lexer to separate the text into tokens  
cutChars = [".", "`","*", "#", 
            "-", ">", "=", "-", 
            "_", "~", "\\", "\n", 
            "$", "[", "]", "(", ")",
            ] + [i for i in range(10)] 

#list of special tokens that will be built by the cleanup fonction 
tokens =[
    "#", "##", "###", "####", "#####", 
    "*", "**", "_", "__", "-", "--", 
    "---", "==", "[", "[[", "]]", "]", 
    "$$", "$", "`", "```", "\\*", 
    "1.", "2.", "3.", "5.", "6.", "7.",
    "7.", "8.", "9."]

#clean up lexed list by tokenizing it 
def Cleanup(lexed):
    global tokens 
    if lexed == []:
        return []

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
        return [tokens[tkn]] + Cleanup(lexed[len(tokens[tkn]):])

    else:
        return [lexed[0]] + Cleanup(lexed[1:])

def Lexer(toParse):
    global cutChars
    o = []
    buffer = u""

    for i in range(len(toParse)):
        if toParse[i] in cutChars:
            if buffer != "":
                o += [buffer, toParse[i]]
            else:
                o += [toParse[i]]
            buffer = u""
        else:
            buffer += toParse[i]
        
    return Cleanup(o)


