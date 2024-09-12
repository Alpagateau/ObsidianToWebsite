import poc


def render(tree):
    value = ""
    footer = ""
    if type(tree) == poc.Node: 
        if tree.tag == "page":
            value = "<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"UTF-8\"> \n</head>\n<body>\n <style>" +  poc.loadFile("POC/poc.css") + "</style>"
            footer = "\n</body>\n</html>"
        else:
            value = tree.tag 

        if tree.tag == "#":
            if tree.children[0][0] == " ":
                value = "<h1>"
                footer = "</h1>\n"
            else:
                value = "<div class=\"tag\">"
                footer = "</div>"

        if tree.tag == "##":
            value = "<h2>"
            footer = "</h2>\n"
        if tree.tag == "###":
            value = "<h3>"
            footer = "</h3>\n"
        
        if tree.tag == "####":
            value = "<h4>"
            footer = "</h4>\n"
        if tree.tag == "#####":
            value = "<h5>"
            footer = "</h5>\n"

        if tree.tag == "*" or tree.tag == "_":
            value = "<i>"
            footer = "</i>"
        
        if tree.tag == "**" or tree.tag == "__":
            value = "<strong>"
            footer = "</strong>"

        if tree.tag == "bl":
            value = "<br>"
        if tree.tag == "bbl":
            value = "<br><br>"

        return value + "".join([render(i) for i in tree.children]) + footer 
    else:
        return tree
"""
print(
    render(
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
