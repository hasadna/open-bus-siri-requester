import os
import sys
import time
import requests
import contextlib
import subprocess

from . import config


REQUEST_URL_TEMPLATE = "http://moran.mot.gov.il:110/Channels/HTTPChannel/SmQuery/2.8/json?Key={Key}&MonitoringRef=AllActiveTripsFilter&StopVisitDetailLevel=normal"


@contextlib.contextmanager
def start_ssh_tunnel():
    if config.OPEN_BUS_SSH_TUNNEL_PRIVATE_KEY_FILE and config.OPEN_BUS_SSH_TUNNEL_SERVER_IP:
        # print("Starting Open Bus SSH Tunnel ({})".format(config.OPEN_BUS_SSH_TUNNEL_SERVER_IP), file=sys.stderr)
        filemode = oct(os.stat(config.OPEN_BUS_SSH_TUNNEL_PRIVATE_KEY_FILE).st_mode)[-3:]
        if filemode not in ['600', '400']:
            # print("Changing key file permissions", file=sys.stderr)
            ret, out = subprocess.getstatusoutput('chmod 400 {}'.format(config.OPEN_BUS_SSH_TUNNEL_PRIVATE_KEY_FILE))
            assert ret == 0, out
        p = subprocess.Popen([
            'ssh', '-q', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no',
            '-D', '127.0.0.1:8123', '-C', '-N', '-i', config.OPEN_BUS_SSH_TUNNEL_PRIVATE_KEY_FILE,
            'sshtunnel@{}'.format(config.OPEN_BUS_SSH_TUNNEL_SERVER_IP)
        ])
        time.sleep(1)
        try:
            yield {
                'http': 'socks5h://127.0.0.1:8123',
                'https': 'socks5h://127.0.0.1:8123'
            }
        finally:
            p.terminate()
    else:
        print("Not using SSH Tunnel, connecting to MOT server directly (will not work if your IP is not allowed)", file=sys.stderr)
        yield None


def request():
    assert config.OPEN_BUS_MOT_KEY, 'missing OPEN_BUS_MOT_KEY config'
    request_url = REQUEST_URL_TEMPLATE.format(Key=config.OPEN_BUS_MOT_KEY)
    with start_ssh_tunnel() as proxies:
        return requests.get(request_url, proxies=proxies).json()
