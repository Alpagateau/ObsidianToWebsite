# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from parser.utils import *
from parser.lexer import *
from parser.parser import *
from parser.renderer import *
import glob
import os

hostName = "localhost"
serverPort = 6969

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        currentPath = self.path.replace("%20", " ") \
                                .replace("%C3%A9", "é") \
                                .replace("%C3%B4", "ô") \
                                .replace("%C3%A8", "è")
        finalPath = ""
        errorMsg = ""
        #print("Current path : " + currentPath)
        filename, ext = GetFileName(currentPath)
        if ext == "md":
            finalPath = "./Revisions" + currentPath 
        elif ext == "css":
            finalPath = "./wserver/style" + currentPath
        elif ext in IMAGE_EXT:
            finalPath = "./Revisions/Média/" + filename + "." + ext
        else:
            errorMsg = """
            <head>
                <meta charset=\"UTF-8\">
            </head> 
            no extension found, do you mean <a href = \"""" + currentPath + ".md \">this ?</a>"       
        if finalPath != "":
            if ext == "md":
                self.send_header("Content-type", "text/html")
                self.end_headers()
                tree = BuildTree(
                    Lexer(
                        LoadFile(finalPath)
                    )
                )
                #PrintTree(tree)
                self.wfile.write(bytes(render(tree, pagename = filename),"utf-8"))
            elif ext == "css":
                #print("Sent the css")
                self.send_header("Content-type", "text/css")
                self.end_headers()

                self.wfile.write(bytes(LoadFile(finalPath), "utf-8"))
            elif ext.lower() in IMAGE_EXT:
                typ = ""
                if ext == "png":
                    typ = "png"
                elif ext in ["jpg","jpg", "jfif", "pjpeg", "pjp"]:
                    typ = "jpeg"
                else:
                    typ = "gif"
                self.send_header("Content-type", "image/" + typ)
                self.end_headers()

                self.wfile.write(LoadBinary(finalPath))
            else:
                self.send_header("Content-type", "text/html")
                self.end_headers()

                self.wfile.write(bytes("404 : " + finalPath, "utf-8"))
        else:
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(bytes("404 : Page Not Found sowwy <br>" + currentPath + "<br>","utf-8"))
            self.wfile.write(bytes(errorMsg,"utf-8"))
        

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")
