import json

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream

from pelita.datamodel import Food, Wall
from pelita.messaging.json_convert import json_converter

ioloop.install()



class MainHandler(tornado.web.RequestHandler):
    def get(self, path):
        p = "../../../webapp/" + path
        #self.render("../../../webapp/" + path) # "index.html")
        print(path)
        with open("webapp/" + path, 'rb') as f:
            while 1:
                data = f.read(16384) # or some other nice-sized chunk
                if not data: break
                self.write(data)
            self.finish()

socket_connections = []

class ZMQSubscriber:
    def __init__(self, context, port):
        self.sock = context.socket(zmq.SUB)
        self.sock.connect("tcp://127.0.0.1:%d" % port)
        self.sock.setsockopt_string(zmq.SUBSCRIBE, "")

        stream = ZMQStream(self.sock)
        stream.on_recv(self.send_data)

        self.walls = None

    def send_data(self, msg):
        processed = self.process_message(msg[0].decode('utf-8'))
        for socket in socket_connections:
            socket.write_message(processed)

    def process_message(self, msg):
        msg_objs = json_converter.loads(msg)

        data = msg_objs.get("__data__") or {}

        universe = data.get("universe")
        game_state = data.get("game_state")
        if universe:

            if not self.walls:
                self.walls = []
                for x in range(universe.maze.width):
                    col = []
                    for y in range(universe.maze.height):
                        col += [Wall in universe.maze[x, y]]
                    self.walls.append(col)

            food = []
            for x in range(universe.maze.width):
                col = []
                for y in range(universe.maze.height):
                    col += [Food in universe.maze[x, y]]
                food.append(col)

            width = universe.maze.width
            height = universe.maze.height

            bots = []
            for bot in universe.bots:
                bot_data = {'x': bot.current_pos[0],
                            'y': bot.current_pos[1]
                           }
                bots.append(bot_data)

            teams = [{"name": t.name, "score": t.score} for t in universe.teams]

            data = {'walls': self.walls,
                    'width': width,
                    'height': height,
                    'bots': bots,
                    'food': food,
                    'teams': teams,
                    'state': game_state
                    }
            data_json = json.dumps(data)
            return data_json


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('new connection')
        #self.write_message("Hello World")
        socket_connections.append(self)

    def on_message(self, message):
        print ('message received %s' % message)

    def on_close(self):
        socket_connections.remove(self)
        print ('connection closed')


def run_server(zmq_port=51001, browser_port=8000):
    context = zmq.Context()

    application = tornado.web.Application([
#        (r"/index.html", tornado.web.StaticFileHandler, {"path": "."}),
        (r"/ws", WSHandler),
        (r"/(.*)", MainHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(browser_port)

    zmq_subscriber = ZMQSubscriber(context, zmq_port)
    tornado.ioloop.IOLoop.instance().start()

run_server()
