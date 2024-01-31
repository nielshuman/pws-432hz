from http.server import SimpleHTTPRequestHandler
import re

class ByteRangeHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()

    def translate_path(self, path):
        path = super().translate_path(path)
        return path

if __name__ == '__main__':
    from http.server import HTTPServer
    import sys

    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    server_address = ('', port)

    httpd = HTTPServer(server_address, ByteRangeHTTPRequestHandler)
    print(f'Serving on port {port}')
    httpd.serve_forever()
