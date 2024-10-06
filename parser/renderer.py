import parser.parser as ps #for symplicity
import parser.utils as ut

simpleCor = {
    #"#"     : ("<h1>"   , "</h1>"   ), #cant use this one because it's also used for tags
    "h2"    : ("<h2>"        , "</h2>"   ),
    "h3"    : ("<h3>"        , "</h3>"   ),
    "h4"    : ("<h4>"        , "</h4>"   ),
    "h5"    : ("<h5>"        , "</h5>"   ),
    "br"    : ("<br>"        , ""        ),
    "*"     : ("<i>"         , "</i>"    ),
    "**"    : ("<b>"         , "</b>"    ),
    "=="    : ("<mark>"      , "</mark>" ),
    "~~"    : ("<s>"         , "</s>"    ),
    "$"     : ("\\("         , "\\)"     ),
    "$$"    : ("\\["         , "\\]"     ),
    "ls"    : ("<ul>"        , "</ul>"   ),
    "le"    : ("<li>"        , "</li>"   ),
    "()"    : ("("           , ")"       ),
    "[]"    : ("["           , "]"       ),
    "---"   : ("<hr/>"       , ""        ),
    "^"     : ('<div class="tag">', "</div>"),
    ">"     : ("<blockquote>", "</blockquote>"),
    "cbu"   : ("<input type=\"checkbox\" disabled value=1/>", ""),
    "cbc"   : ("<input type=\"checkbox\" disabled checked value=1/>", ""),
}

def buildList(current=""):
    # load cached file list
    ls = ut.LoadFile("./Cache/filelist.txt")
    dic = {}
    ls = ls.split("\n")
    for i in range(len(ls)):
        temp = ls[i].split(",")
        if len(temp) > 1:
            dic[temp[0]] = temp[1]
    #build file list html
    content = "<ul>"
    for k in dic.keys():
        content += "<li><a href = \"/" + dic[k] + "\">" + k.replace(".md", "") + "</a></li>"
    content += "</ul>"
    return content

def render(tree, pagename = "", minimized = False):
    global simpleCor 
    value = ""
    footer = ""
    if type(tree) == ps.Node: 
        if tree.tag == "page":
            if not minimized:
                value = ut.LoadFile("./wserver/defaultPage.html")
            else:
                value = ut.LoadFile("./wserver/minhtml.html")
            footer = value[value.find("¤")+1:] 
            value = value[:value.find("¤")] + "<div class=\"pageTitle\">" + pagename + "</div>"
            value= value.replace("ߡ", pagename).replace("_sidelist_", buildList())
            #print(value)
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
                if "#" in adress:
                    adress = adress[ adress.find("#"):]
                value = "<a href = \"" + adress + ".md\">" + name 
                footer = "</a>"
                tree.children = []
            else:
                if "#" in tree.children[0]:
                    value = "<strong>" + tree.children[0].replace("#", "") + "</strong>"
                    tree.children = []
                else:
                    value = "<a href=\"" + tree.children[0] + ".md\">" + tree.children[0]
                    footer = "</a>"
                    tree.children = []
        
        if tree.tag == "![[]]":
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
                name, ext = ut.GetFileName(adress)
                if ext in ut.IMAGE_EXT:
                    value = "<img src = \"" + adress + "\"width = \"" + name + "px\">" 
                    footer = ""
                else:
                    value = "<iframe src=\"" + adress + ".md%\">"
                    footer = "</iframe>"
                tree.children = []
            else:
                name, ext = ut.GetFileName(tree.children[0]) 
                if ext in ut.IMAGE_EXT:
                    value = "<img src=\"" + tree.children[0] + "\">"
                    footer = ""
                else:
                    value = "<iframe src=\"" + tree.children[0] + ".md%\">"
                    footer = "</iframe>"
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

        

        #table handling 
        if tree.tag == "table":
            headers = tree.children[0].children[0]
            data = tree.children[1]
            value = "<table><tr>"
            footer = "</table>"
            
            for i in range(len(headers.children)):
                value += "<th>" + "".join(render(x) for x in headers.children[i].children) + "</th>"
            value += "</tr>\n"
            for i in range(len(data.children)):
                value += "<tr>"
                for j in range(len(data.children[i].children)):
                    value += "<td>" + "".join([render(i) for i in data.children[i].children[j].children]) + "</td>\n"
                value += "</tr>\n"
            return value + footer 
        #print(type(value), type(footer))
        return value + "".join([render(i) for i in tree.children]) + footer 
    else:
        if type(tree) == type([0,0]):
            return "".join(tree)
        else:
            return tree

