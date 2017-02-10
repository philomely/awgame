# from gevent.server import StreamServer
#
# def handler(socket , address):
#     print("new connection from %s:%s" % address)
#     socket.sendall(b'hello')
# if __name__ == "__main__":
#     server = StreamServer(("0.0.0.0", 16000), handler)
#     print('starting echo server on port 16000')
#     server.serve_forever()

import gevent
import random
import json

from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

rooms = {}

class AdvancedWarsApplication(WebSocketApplication):
    def on_open(self):
        self.ws.send("welcome")
        gevent.sleep(0.1)

    def on_message(self, message):
        print(message)
        #self.ws.send(message)
        #self.broadcast(message)
        msg = json.loads(message)
        self.process_message(msg)

    def process_message(self, msg):
        msgid = msg.get("msgid")
        if msgid == "create_room":
            self.create_room(msg.get("userid"))
        elif msgid == "join_room":
            self.join_room(msg.get("userid"))

    def create_room(self, userid):
        currentClient = self.ws.handler.active_client
        l = []
        l.append(userid)
        rooms[userid] = \
            {"gamers": l}
        self.ws.send(json.dumps(rooms[userid]))

    def join_room(self, userid):
        for room in rooms:
            if len(room["gamers"]) == 1:
                room["gamers"].append(userid)
                self.ws.send(room)
                break

    def on_close(self, reason):
        print(reason)

    def send_client_list(self, message):
        current_client = self.ws.handler.active_client
        current_client.nickname = message['nickname']

        self.ws.send(json.dumps({
            'msg_type': 'update_clients',
            'clients': [
                getattr(client, 'nickname', 'anonymous')
                for client in self.ws.handler.server.clients.values()
            ]
        }))

    def broadcast(self, message):
        for client in self.ws.handler.server.clients.values():
            print(client)
            client.ws.send(json.dumps({
                'msg_type': 'message',
                'nickname': message['nickname'],
                'message': message['message']
            }))

def static_wsgi_app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/html")])
    return open("plot_graph.html").readlines()


resource = Resource([
    ('/', static_wsgi_app),
    ('/aw', AdvancedWarsApplication)
])

if __name__ == "__main__":
    server = WebSocketServer(('', 8000), resource, debug=True)
    server.serve_forever()