from gevent.server import StreamServer

def handler(socket , address):
    print("new connection from %s:%s" % address)
    socket.sendall(b'hello')
if __name__ == "__main__":
    server = StreamServer(("0.0.0.0", 16000), handler)
    print('starting echo server on port 16000')
    server.serve_forever()