from http.server import ThreadingHTTPServer
from http.server import BaseHTTPRequestHandler

from . import config
from . import storage


class HealthDaemonHTTPRequestHandler(BaseHTTPRequestHandler):

    def _send_ok(self, msg='OK'):
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(msg.encode())

    def _send_error(self, error='Server Error', status_code=500):
        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(error.encode())

    def do_GET(self):
        seconds_since_last_snapshot = storage.get_seconds_since_last_snapshot()
        msg = '{} seconds since last snapshot'.format(seconds_since_last_snapshot)
        if seconds_since_last_snapshot > config.HEALTH_DAEMON_MAX_SECONDS_SINCE_LAST_SNAPSHOT:
            self._send_error(error='ERROR: ' + msg)
        else:
            self._send_ok(msg='OK: ' + msg)


class HealthDaemonHTTPServer(ThreadingHTTPServer):

    def __init__(self):
        print("Starting health daemon on port {}".format(config.HEALTH_DAEMON_PORT))
        super(HealthDaemonHTTPServer, self).__init__(('0.0.0.0', config.HEALTH_DAEMON_PORT), HealthDaemonHTTPRequestHandler)


def start():
    HealthDaemonHTTPServer().serve_forever()
