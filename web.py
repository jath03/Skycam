import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import websockets
import asyncio
import os
from functools import partial

async def handler(skycam, websocket, path):
    while True:
        value = await websocket.recv()
        print("Websocket>> recieved " + value)
        if "drive" in value and not "?" in value:
            await websocket.send(str(skycam.move(value.split(',')[1])))
        elif "drive" in value and "?" in value:
            await websocket.send(skycam.move())
        elif "pan" in value and not "?" in value:
            await websocket.send(str(skycam.pan(value.split(',')[1])))
        elif "pan" in value and "?" in value:
            await websocket.send(skycam.pan())
        if "tilt" in value and not "?" in value:
            await websocket.send(str(skycam.tilt(value.split(',')[1])))
        elif "tilt" in value and "?" in value:
            await websocket.send(skycam.tilt())

        await asyncio.sleep(.1)


def main(skycam):
    start_server = websockets.serve(partial(handler, skycam), '192.168.5.14', 7000)
    os.chdir(os.path.join(os.path.dirname(__file__), 'app'))
    httpd = HTTPServer(('192.168.5.14', 9000), SimpleHTTPRequestHandler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    print("running http server")
    server_thread.start()
    print("running websocket server")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
