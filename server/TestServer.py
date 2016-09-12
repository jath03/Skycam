from http.server import BaseHTTPRequestHandler, HTTPServer
import threading, pickle, re, subprocess, urllib, os
    
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        f_type_map = {'.html': 'text/html', '.css': 'text/css', '.ico': 'image/x-icon', '.jpg': 'image/jpeg', '.png': 'image/png', '.gif': 'image/gif', '.js': 'application/javascript', '.py': 'application/python'}
        t_type = re.compile('\/|(\.\w*)')
        r_file = self.path.split('?')
        requested_type = t_type.findall(self.path)
        ex = requested_type[-1]
        hds = []
        if ex != '.py':
            
            try:
                res = 200
                f = None
                hds = [('Content-type', f_type_map[ex]), ('Content-Encoding', 'utf-8')]
                try:
                    with open('/home/jack/projects/Skycam/server%s'% r_file[0]) as file:
                        f = file.read()
                        #f = 'This is my secret message'
                        #self.wfile.write(bytes(f, 'utf8'))
                except UnicodeDecodeError:
                    with open('/home/jack/projects/Skycam/server%s'% r_file[0], 'rb') as file:
                        f = file.read()
                        #self.wfile.write(f)
            except IOError:
                res = 404
                f = None
                #self.send_error(404, 'File Not Found')
                #self.wfile.write(bytes('404 file not found', 'utf8'))
            except KeyError:
                #self.send_response(200)
                #self.send_header('Content-type', 'text/html')
                #self.end_headers()
                with open('/home/jack/projects/Skycam/server/index.html') as file:
                    #f = 'This is my secret message'
                    f = file.read()
                    #self.wfile.write(bytes(f, 'utf8'))
                    hds = [('Content-type', 'text/html'), ('Content-Encoding', 'utf-8')]
            if res == 200:
                self.send_response(res)
            else:
                self.send_error(res)
            for item in hds:
                i1, i2 = item
                self.send_header(i1, i2)
            self.end_headers()
            if f != None:
                    try:
                        self.wfile.write(f)
                    except: 
                        self.wfile.write(f.encode('utf-8'))
            else:
                pass
            return
        else:
            
            file = subprocess.run(['python', '/home/jack/projects/msc_testing%s'% r_file[0]], stdout=subprocess.PIPE)
            self.wfile.write(file.stdout)
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        with open('params.dat', 'wb') as f:
            pickle.dump(post_data, f)
#        file = subprocess.run(['python', '/home/jack/projects/msc_testing%s'% r_file[0]], stdout=subprocess.PIPE)
        self.send_response(200)
        self.end_headers()
        self.wfile.write('file recieved'.encode('utf-8'))
    def do_OPTIONS(self):
        methods = ['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE']
        sup_methods = []
        self.send_response(200)
        for m in methods:
            if hasattr(self, 'do_' + m):
                sup_methods.append(m)
            else:
                pass
        print(sup_methods)
        meth = ', '.join(sup_methods)
        self.send_header('Allow', meth)
        self.end_headers() 


server_address = ('192.168.1.200', 6789)
def run():
    print('starting server ...')
    httpd = HTTPServer(server_address, MyHandler)
    httpd.serve_forever()
	
bg_server= threading.Thread(target = run)

if __name__ == '__main__':
    bg_server.start()
    print('\nserver started at %s:%s'% server_address)

