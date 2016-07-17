from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import pickle
    
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('/home/jack/projects/skycam/main/Skycam/skycam-page.html', 'r') as test:
            f = test.read()
        with open('/home/jack/projects/skycam/main/Skycam/style.css', 'r') as style:
        #ms = str(webinterface())
            f2 = style.read()
            self.wfile.write(bytes(f2, 'utf8'))
        self.wfile.write(bytes(f, 'utf8'))
        #self.wfile.write(bytes('<html><head><title>site</title></head>', 'utf8'))
        #self.wfile.write(bytes('<body><p>Hello world</p></body></html>', 'utf8'))
        return
def run():
    print('starting server ...')
    server_address = ('192.168.1.150', 7777)
    httpd = HTTPServer(server_address, MyHandler)
    print('running server...')
    httpd.serve_forever()
bg_server= threading.Thread(target = run)
###Uncomment the next line if you want to have the server start when the file is run###
#bg_server.start()
