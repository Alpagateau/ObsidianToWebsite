import parser.parser as ps #for symplicity
import parser.utils as ut

simpleCor = {
    #"#"     : ("<h1>"   , "</h1>"   ), #cant use this one because it's also used for tags
    "h2"    : ("<h2>"   , "</h2>"   ),
    "h3"    : ("<h3>"   , "</h3>"   ),
    "h4"    : ("<h4>"   , "</h4>"   ),
    "h5"    : ("<h5>"   , "</h5>"   ),
    "br"    : ("<br>"   , ""        ),
    "*"     : ("<i>"    , "</i>"    ),
    "**"    : ("<b>"    , "</b>"    ),
    "=="    : ("<mark>" , "</mark>" ),
    "~~"    : ("<s>"    , "</s>"    ),
    "$"     : ("\\("    , "\\)"     ),
    "$$"    : ("\\["    , "\\]"     ),
    "ls"    : ("<ul>"   , "</ul>"   ),
    "le"    : ("<li>"   , "</li>"   ),
}

def render(tree):
    global simpleCor 
    value = ""
    footer = ""
    if type(tree) == ps.Node: 
        if tree.tag == "page":
            value = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset=\"UTF-8\">
                
                <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
                
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/night-owl.css">
                
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/go.min.js"></script>
                <script>hljs.highlightAll();</script>
            </head>
            <body>
                <style>""" +  ut.LoadFile("POC/poc.css") + "</style>" + """
                <div class=\"middle\">
                """
            footer = "\n</div>\n</body>\n</html>"
        else:
            value = tree.tag 
        
        if tree.tag == "h1":
            if tree.children[0][0] == " ":
                value = "<h1>"
                footer = "</h1>\n"
            else:
                value = "<div class=\"tag\">"
                footer = "</div>"
        
        if tree.tag in simpleCor.keys():
            value, footer = simpleCor[tree.tag]
        
        if tree.tag == "***":
            value = "<strong><i>"
            footer = "</i></strong>"
        '''
        if tree.tag == "bl":
            value = "<br>"
        if tree.tag == "bbl":
            value = "<br><br>"
        '''
        if tree.tag == "[[]]":
            if "|" in tree.children[0]:
                #split the name and the url 
                adress = ""
                name = ""
                passed = False 
                for i in range(len(tree.children[0])):
                    if tree.children[0][i] == "|":
                        passed = True 
                        continue 
                    if passed:
                        name += tree.children[0][i]
                    else:
                        adress += tree.children[0][i]
                value = "<a href = \"" + adress + "\">" + name 
                footer = "</a>"
                tree.children = []
            else:
                value = "<a href=\"" + tree.children[0] + "\">" + tree.children[0]
                footer = "</a>"
                tree.children = []

        
        if tree.tag == "```":
            language = ""
            i = 0
            while tree.children[0][i] != "\n":
                language += tree.children[0][i]
                i += 1
            tree.children[0] = tree.children[0][i+1:]
            value = "<pre><code class = \"language-"+language+"\">"
            footer = "</code></pre>"

        if tree.tag == "wl":
            value = "<a href = \"" + tree.children[0] + "\" >" + tree.children[1] + "</a>"
            tree.children = []
        return value + "".join([render(i) for i in tree.children]) + footer 
    else:
        return tree

