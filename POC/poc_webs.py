# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import poc_render as pr
import treeCleaner as tc
import glob
import os

hostName = "localhost"
serverPort = 6969

DIRS = [ "./Revisions/", "./Revisions/Cours/", "./Revisions/Exercices/", "./Revisions/Preuves"]

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        currentPath = self.path.replace("%20", " ").replace("%C3%A9", "é")
        finalPath = ""
        errorMsg = ""
        if currentPath[-3:] == ".md":
            finalPath = currentPath 
        else:
            for i in range(len(DIRS)):
                if os.path.exists(DIRS[i] + currentPath + ".md"):
                    finalPath = DIRS[i] + currentPath + ".md"
                    break 
                else:
                    errorMsg += "Not in : " + DIRS[i] + "\n<br>"
        #print(self.path)
        
        if finalPath != "":
            tree = tc.TreeShaker(
                pr.poc.TreeBuilder(
                    pr.poc.Cleanup(
                        pr.poc.Lexer(
                            pr.poc.loadFile(finalPath)
                        )
                    )
                )
            )
            pr.poc.printTree(tree)
            self.wfile.write(bytes(pr.render(tree),"utf-8"))
        else:
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
