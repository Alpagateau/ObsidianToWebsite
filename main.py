from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from parser.utils import *
from parser.lexer import *
from parser.parser import *
from parser.renderer import *
#from wserver.search import *
import os
import ssl
import sys
from startup import *

hostName = "localhost"
serverPort = 6969

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print("GET is ok")
        response = Direct(self.path)

        self.send_response(response["code"])
        self.send_header(response["hprefix"], response["hcontent"])
        self.end_headers()

        if response["code"] == 200:
            if response["ext"] == "md":
                tree = BuildTree(Lexer(LoadFile(response["path"])))
                self.wfile.write(
                    bytes(render(
                        tree, 
                        pagename = response["filename"], 
                        minimized = response["min"]
                    ) ,"utf-8") )

            elif response["ext"] == "css":
                self.wfile.write( bytes(LoadFile(response["path"]), "utf-8") )
            elif response["ext"] == "search":
                self.wfile.write( bytes(Search(response["filename"]),"utf-8"))
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
        "ext" : "",
        "min": False 
    }

#    if "?" in currentPath:
#        querry = currentPath.split("?")[-1]
#        response["ext"] = "search"
#        response["filename"] = querry
#        return response
    if currentPath[-1] == "%":
        response["min"] = True
        currentPath = currentPath[:-1]
    
    if rpath=="/":
        response["code"] = 301
        response["hprefix"] = "Location"
        response["hcontent"] = "index.md"
        response["ext"] = "md"
        return response 
    
    if rpath=="/favicon.ico":
        response["code"] = 200
        response["hprefix"] = "Content-type"
        response["hcontent"] = "image/ico"
        response["ext"] = "ico"
        response["path"] = "./wserver/book.ico"
    
    if rpath=="/test.md":
        response["code"] = 200
        response["hprefix"] = "Content-type"
        response["hcontent"] = "text/html"
        response["ext"] = "md"
        response["path"] = "./POC/test.md"
        return response

    filename, ext = GetFileName(currentPath)
    response["filename"] = filename
    response["ext"] = ext 
    
    mockup = "/" + filename+"."+ext

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
            print(currentPath + " is in cours")
            response["code"] = 301
            response["hprefix"] = "Location"
            response["hcontent"] = "/Cours" + currentPath
            response["path"] = ""
        elif os.path.exists("./Revisions/Preuves" + mockup):
            response["code"] = 301
            response["hprefix"] = "Location"
            response["hcontent"] = "/Preuves" + mockup + ("" if not response["min"] else "%")
            response["path"] = ""
            print("Are we even here ?")
        else:
            print("Could not find " + currentPath)
            response["code"] = 404
            response["err"] = "File " + currentPath + " not found"
    return response

if __name__ == "__main__":        
    UpdateFileList() 
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")
    
    """ 
    server_adress = (hostName, serverPort)
    httpd = HTTPServer(server_adress, MyServer)

    httpd.socket = ssl.wrap_socket(httpd.socket,  certfile='server.crt',keyfile='server.key',server_side=False)
    
    print("Server started on https://%s:%s" % (hostName, serverPort))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass 
    httpd.server_close()
    print("Server stopped")
    """

