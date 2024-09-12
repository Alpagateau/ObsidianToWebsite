# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import poc_render as pr
hostName = "localhost"
serverPort = 8081

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(
            pr.render(
                pr.render(
                    pr.poc.TreeBuilder(
                        pr.poc.Cleanup(
                            pr.poc.Lexer(
                                pr.poc.loadFile("RemarkablePOC/index.md")
                            )
                        )
                    )
                )
            )
            ,"utf-8"))
        """
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        """
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")