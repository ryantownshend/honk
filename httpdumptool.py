#!/usr/bin/env python
# Reflects the requests from HTTP methods GET, POST, PUT, and DELETE

# try 3: except 2
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

from optparse import OptionParser

# https://docs.python.org/2/library/basehttpserver.html?highlight=basehttprequesthandler#BaseHTTPServer.BaseHTTPRequestHandler


def query_split(path):
    o = urlparse(path)
    query_str = o.query
    d = parse_qs(query_str)
    return d


class RequestHandler(BaseHTTPRequestHandler):

    def output_start(self):
        print("--- %s Request Start" % self.command)

    def output_client_ip(self):
        print("client ip : %s" % (self.client_address[0]))

    def output_end(self):
        print("")

    def output_path(self):
        print("path : %s " % self.path)

    def output_queries(self):
        print("queries :")
        queries = query_split(self.path)
        for item in queries:
            print("  - %s : %s" % (item, queries[item]))

    def output_headers(self):
        print("headers :")
        for item in self.headers:
            print("  - %s : %s" % (item, self.headers[item]))

    def output_body(self):
        print("body : >")
        content_length = self.headers.get('content-length')
        print(content_length)
        length = int(content_length) if content_length else 0
        body_str = self.rfile.read(length)

        try:
            data = body_str.decode()
            print(data)
        except AttributeError:
            print(body_str)

    def do_GET(self):
        self.output_start()
        self.output_path()
        self.output_client_ip()
        self.output_queries()
        self.output_headers()
        self.send_response(200)
        self.end_headers()
        self.output_end()

    def do_POST(self):
        self.output_start()
        self.output_path()
        self.output_client_ip()
        self.output_queries()
        self.output_headers()
        self.output_body()
        self.send_response(200)
        self.end_headers()
        self.output_end()

    do_PUT = do_POST
    do_DELETE = do_GET

    def log_message(self, format, *args):
        return


def main():
    parser = OptionParser()
    parser.add_option(
        "-p",
        "--port",
        dest="port",
        help="port to listen on, defaults to 8080",
        metavar="PORT",
        default=8080,
        type="int"
    )
    parser.usage = (
        "Creates a server that will echo out any GET or POST parameters\n"
    )
    (options, args) = parser.parse_args()

    port = options.port
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
