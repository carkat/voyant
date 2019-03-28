#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import json

### https://daanlenaerts.com/blog/2015/06/03/create-a-simple-http-server-with-python-3/
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

      # GET
    def fizzbuzz_get(self,query):
        ## TODO: Should add error handling here for malformed arguments
        pairs     = query.split('%26')
        args      = [int(arg.split('=')[1]) for arg in pairs]

        # get fizzbuzz results
        [begin, end] = args
        result = json.dumps({'result': fizzbuzz(begin, end)})

        # Send message back to client
        # Write content as utf-8 data
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(bytes(result, 'utf-8'))

    def do_GET(self):
        url_parts = urlparse.urlparse(self.path)
        if url_parts.path == '/fizzbuzz':
            self.fizzbuzz_get(url_parts.query)

        self.send_response(404)
        return
    
### Begin Fizzbuzz code
### A fun functional means of generating fizzbuzz
def str_if_divisible(n, string):
    '''Return a function which takes in a fizzbuzz number
    Then ask, is the fizzbuzz number divisible by n? if so return string
    Otherwise return an empty string
    '''
    return lambda x: string if x % n == 0 else ''

def str_or_n(n,string):
    '''If the string is not empty return it, othwerise return the 
    fizzbuzz number n
    '''
    return string if string else n

def fizzbuzz(begin,end):
    '''div 3 and 5 are both functions waiting for a fizzbuzz number, and which
    return an empty string, or the second argument. We then mep string or number
    over the range from begin to end. 
    '''
    div3   = str_if_divisible(3, 'fizz')
    div5   = str_if_divisible(5, 'buzz')
    return [str_or_n(n, div3(n) + div5(n)) for n in range(begin, end)]


if __name__ == '__main__':
    print('starting server...')
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()
