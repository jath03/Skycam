import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import websockets
import asyncio
import os

async def handler(websocket, path):
    while True:
        await websocket.send("hi")
        value = await websocket.recv()
        print("Websocket>> recieved " + value)
        if "drive" in value and not "?" in value:
            # skycam.move(value.split(',')[1])
            await websocket.send(value.split(',')[1])
        elif "drive" in value and "?" in value:
            # websocket.send(skycam.move())
            await websocket.send("1")
        elif "pan" in value and not "?" in value:
            # skycam.pan(value.split())
            pass
        await asyncio.sleep(.1)


def main():
    start_server = websockets.serve(handler, 'localhost', 7000)
    os.chdir(os.path.join(os.path.dirname(__file__), 'app'))
    httpd = HTTPServer(('', 9000), SimpleHTTPRequestHandler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    print("running http server")
    server_thread.start()
    print("running websocket server")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
