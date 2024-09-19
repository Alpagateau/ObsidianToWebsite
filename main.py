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
        response = Direct(self.path)

        self.send_response(response["code"])
        self.send_header(response["hprefix"], response["hcontent"])
        self.end_headers()

        if response["code"] == 200:
            if response["ext"] == "md":
                tree = BuildTree(Lexer(LoadFile(response["path"])))
                self.wfile.write( bytes( render(tree, pagename = response["filename"]) ,"utf-8") )
            
            elif response["ext"] == "css":
                self.wfile.write( bytes(LoadFile(response["path"]), "utf-8") )
            else:
                self.wfile.write( LoadBinary(response["path"]) )

def Direct(rpath):
    currentPath = rpath.replace("%20", " ")     \
        .replace("%C3%A9", "é") \
        .replace("%C3%B4", "ô") \
        .replace("%C3%A8", "è") \
        .replace("%E9", "é") \
        .replace("%E8", "è") \
    
    response = {
        "code" : 200,
        "hprefix" : "Content-type",
        "hcontent": "text/html",
        "path" : "./Revisions",
        "err"  : "",
        "filename" : "",
        "ext" : ""
    }
    
    filename, ext = GetFileName(currentPath)
    response["filename"] = filename
    response["ext"] = ext 
    if ext == "css":
        response["hcontent"] = "text/css"
        response["path"] = "./wserver/style" + currentPath 
    elif ext == "png":
        response["hcontent"] = "image/png"
        response["path"] = "./Revisions/Média/" + response["filename"] + "." + response["ext"]
    elif ext == "jpg":
        response["hcontent"] = "image/jpg"
        response["path"] = "./Revisions/Média/" + response["filename"] + "." + response["ext"]
    #add more image type as you go ^^
    elif ext == "md":
       #check if file exist
        if os.path.exists("./Revisions" + currentPath):
            response["path"] = "./Revisions" + currentPath
        elif os.path.exists("./Revisions/Cours" + currentPath):
            response["code"] = 301
            response["hprefix"] = "Location"
            response["hcontent"] = "/Cours" + currentPath
            response["path"] = ""
        else:
            response["code"] = 404
            response["err"] = "File " + currentPath + " not found"
    return response

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")
