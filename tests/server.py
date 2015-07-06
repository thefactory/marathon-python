__author__ = 'kevinschoon@gmail.com'

import os
import json
import sys

if sys.version_info[0] == 3:
    from http.server import SimpleHTTPRequestHandler as HTTPHandler
    from socketserver import TCPServer
else:
    from SimpleHTTPServer import SimpleHTTPRequestHandler as HTTPHandler
    from SocketServer import TCPServer


class Handler(HTTPHandler):
    posts = list()

    def do_POST(self):
        length = int(self.headers['content-length'])
        self.posts.append(json.loads(self.rfile.read(length).decode('UTF-8')))
        self.send_response(code=200)


class EventListener:
    """
    EventListener is used to collect events from the Marathon eventbus.
    """

    def __init__(self, request_count=100, port=9999, path='.', queue=None):
        self.request_count = request_count
        self.queue = queue
        self.port = port
        self.httpd = TCPServer(("", self.port), Handler)
        self.path = os.path.abspath(path) + '/marathon_log.json'
        self.counter = 0
        print('Server listening on port {}'.format(port))

    def log_output(self):
        print('Processed {} requests'.format(self.counter))

    def get_requests(self):
        responses = list()
        while True:
            self.httpd.handle_request()
            self.counter += 1
            self.log_output()
            response = self.httpd.RequestHandlerClass.posts.pop()
            if self.queue:
                self.queue.put(response)
            else:
                responses.append(response)
            if self.counter >= self.request_count:
                break
        return responses

    def record_requests(self):
        with open(self.path, 'w') as fp:
            while self.counter < self.request_count:
                self.httpd.handle_request()
                self.counter += 1
                self.log_output()
                fp.write(json.dumps(self.httpd.RequestHandlerClass.posts.pop()))
