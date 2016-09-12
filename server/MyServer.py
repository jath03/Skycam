from http.server import BaseHTTPRequestHandler, HTTPServer
import threading, pickle, re
    
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        f_type_map = {'.html': 'text/html', '.css': 'text/css', '.ico': 'image/x-icon', '.jpg': 'image/jpeg', '.png': 'image/png', '.gif': 'image/gif', '.js': 'text/javascript'}
        t_type = re.compile('.\w*')
        requested_type = t_type.findall(self.path)
        ex = requested_type[-1]
        try:
            self.send_response(200)
            self.send_header('Content-type', f_type_map[ex])
            self.end_headers()
            try:
                with open('/home/jack/projects/Skycam/server%s'% self.path) as file:
                    f = file.read()
                    self.wfile.write(bytes(f, 'utf8'))
            except UnicodeDecodeError:
                with open('/home/jack/projects/Skycam/server%s'% self.path, 'rb') as f:
                    file = f.read()
                    self.wfile.write(file)
        except IOError:
            self.send_error(404, 'File Not Found')
            self.wfile.write(bytes('404 file not found', 'utf8'))
        except KeyError:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('/home/jack/projects/Skycam/server/skycam-page.html') as file:
                f = file.read()
                self.wfile.write(bytes(f, 'utf8'))
        return
#def run():
#    print('starting server ...')
#    server_address = 
#    httpd = HTTPServer(server_address, MyHandler)
#    httpd.serve_forever()
#	
#bg_server= threading.Thread(target = run)

###Uncomment the next line if you want to have the server start when the file is run###
#bg_server.start()
#print('\nserver started at %s:%s'% server_address)
