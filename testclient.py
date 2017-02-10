import websocket
import _thread
import time
import json

def on_message(ws, message):
    print("on_message")
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        #message = {}
        ws.send(json.dumps({
            'userid': 'aaron',
            'msgid': "create_room",
            'msgdata': ""
        }))
        #ws.close()
    _thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/aw",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()