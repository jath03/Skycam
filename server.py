from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from skycam import  *
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        test = open('c:\\Users\jackt.JACK-IS-AWESOME\Documents\GitHub\jath03.github.io\index.html', 'r')
        mes = test.read()
        ms = webinterface()
        self.wfile.write(bytes(ms, 'utf8'))
        #self.wfile.write(bytes('<html><head><title>site</title></head>', 'utf8'))
        #self.wfile.write(bytes('<body><p>Hello world</p></body></html>', 'utf8'))
        return
def run():
    print('starting server ...')
    server_address = ('192.168.1.42', 9999)
    httpd = HTTPServer(server_address, MyServer)
    print('running server...')
    httpd.serve_forever()
th = threading.Thread(target = run)
th.start()

