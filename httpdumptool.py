#!/usr/bin/env python
#
# Http Ongoing Network Knife
#
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

import click
import click_log
import logging
import json
import yaml
from tabulate import tabulate


log = logging.getLogger(__name__)
click_log.basic_config(log)

# https://docs.python.org/2/library/basehttpserver.html?highlight=basehttprequesthandler#BaseHTTPServer.BaseHTTPRequestHandler

FORMATS = ['json', 'yaml', 'string']


def query_split(path):
    o = urlparse(path)
    query_str = o.query
    d = parse_qs(query_str)
    return d


class RequestHandler(BaseHTTPRequestHandler):
    output_format = "json"
    report_dict = {}
    show_body = False

    def output_start(self):
        self.report_dict['command'] = self.command

    def output_client_ip(self):
        self.report_dict['ip'] = self.client_address[0]

    def output_path(self):
        self.report_dict['full_path'] = self.path
        self.report_dict['base_path'] = urlparse(self.path).path

    def output_queries(self):
        queries = query_split(self.path)
        self.report_dict['queries'] = {}
        for item in queries:
            value = queries[item]
            if isinstance(value, (list, tuple)):
                if len(value) == 1:
                    value = value[0]

            self.report_dict['queries'][item] = value

    def output_headers(self):
        self.report_dict['headers'] = {}
        for item in self.headers:
            self.report_dict['headers'][item] = self.headers[item]

    def output_body(self):
        content_length = self.headers.get('content-length')
        length = int(content_length) if content_length else 0
        body_str = self.rfile.read(length)
        self.report_dict['body_length'] = length
        if self.show_body:
            try:
                data = body_str.decode()
                self.report_dict['body'] = data

            except AttributeError:
                self.report_dict['body'] = body_str

    def do_GET(self):
        self.output_start()
        self.output_path()
        self.output_client_ip()
        self.output_queries()
        self.output_headers()
        self.send_response(200)
        self.report()

    def do_POST(self):
        self.output_start()
        self.output_path()
        self.output_client_ip()
        self.output_queries()
        self.output_headers()
        self.output_body()
        self.send_response(200)
        self.report()

    do_PUT = do_POST
    do_DELETE = do_GET

    def report(self):
        if self.output_format in "json":
            self.report_json()

        elif self.output_format in "yaml":
            self.report_yaml()

        elif self.output_format in "string":
            self.report_string()

    def report_yaml(self):
        print(yaml.dump(self.report_dict, default_flow_style=False))

    def report_json(self):
        print(json.dumps(self.report_dict, indent=4))

    def report_string(self):
        print("command   : %s" % self.report_dict['command'])
        print("ip        : %s" % self.report_dict['ip'])
        print("base path : %s" % self.report_dict['base_path'])
        print(" ")
        h_headers = ['Header', 'Value']
        # flip the code and name and sort
        h_data = sorted(
            [(k, v) for k, v in self.report_dict['headers'].items()])
        print(tabulate(h_data, headers=h_headers))

        print(" ")
        q_headers = ['Param', 'Value']
        # flip the code and name and sort
        q_data = sorted(
            [(k, v) for k, v in self.report_dict['queries'].items()])
        print(tabulate(q_data, headers=q_headers))

        if self.show_body:
            if self.report_dict['body_length'] > 0:
                print("body (length %d):" % self.report_dict['body_length'])
                print(self.report_dict['body'])

    def log_message(self, format, *args):
        return


class Controller(object):

    def __init__(self, port, format_string, body):
        self.port = port
        self.format_string = format_string
        self.show_body = body
        print('Listening on localhost:%s' % self.port)

    def run(self):
        self.server = HTTPServer(('', self.port), RequestHandler)
        self.server.RequestHandlerClass.output_format = self.format_string
        self.server.RequestHandlerClass.show_body = self.show_body

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass


@click.command()
@click.option(
    "-p",
    "--port",
    "port",
    help="port to listen on, defaults to 8080",
    default=8080,
)
@click.option(
    "-f",
    "--format",
    "format_string",
    help="format to output report",
    default="yaml",
    type=click.Choice(FORMATS),
)
@click.option(
    "-b",
    "--body",
    help="show body content",
    is_flag=True
)
@click.pass_context
@click_log.simple_verbosity_option(log)
def main(ctx, port, format_string, body):
    controller = Controller(port, format_string, body)
    controller.run()


if __name__ == "__main__":
    main()
