import os
import sys
import time
import datetime
import traceback

import requests
import contextlib
import subprocess

import pytz

from . import config, storage


REQUEST_URL_TEMPLATE = "http://moran.mot.gov.il:110/Channels/HTTPChannel/SmQuery/2.8/json?Key={Key}&MonitoringRef=AllActiveTripsFilter&StopVisitDetailLevel=normal"
ALT_REQUEST_URL_TEMPLATE = REQUEST_URL_TEMPLATE.replace(':110/', ':1110/')


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
    retry_num = 0
    while True:
        snapshot_data = _request(False)
        if snapshot_data:
            return snapshot_data
        else:
            print("Failed to get snapshot, attempting alternative source...")
            snapshot_data = _request(True)
            if snapshot_data:
                print("Got data from alternative source")
                return snapshot_data
            else:
                print("Failed to get from alternative source")
                if retry_num >= 3:
                    raise Exception("Too many failures to get data from MOT")
                else:
                    retry_num += 1
                    print("Will retry in {} seconds".format(config.OPEN_BUS_REQUESTER_TIMEOUT_SECONDS))
                    time.sleep(config.OPEN_BUS_REQUESTER_TIMEOUT_SECONDS)


def _request(use_alt=False):
    request_url_template = ALT_REQUEST_URL_TEMPLATE if use_alt else REQUEST_URL_TEMPLATE
    request_url = request_url_template.format(Key=config.OPEN_BUS_MOT_KEY)
    with start_ssh_tunnel() as proxies:
        try:
            res = requests.get(
                request_url, proxies=proxies, timeout=config.OPEN_BUS_REQUESTER_TIMEOUT_SECONDS
            )
        except:
            traceback.print_exc()
            res = None
        if not res:
            print("Request failed: unexpected exception")
            return False
        elif res.status_code != 200:
            print("Request failed: invalid status code: {}".format(res.status_code))
            return False
        else:
            try:
                snapshot_data = res.json()
            except:
                traceback.print_exc()
                snapshot_data = None
            if not snapshot_data:
                print("Request failed: unexpected exception trying to get json data")
                return False
            else:
                stats = storage.read_stats(snapshot_data=snapshot_data)
                if stats['failed_to_read']:
                    print("Request failed: failed to parse snapshot data")
                    return False
                elif use_alt and (datetime.datetime.now(pytz.UTC) - stats['response_timestamp']).total_seconds() > 360:
                    print("Request failed: alternative request timestamp is too old")
                    return False
                else:
                    return snapshot_data
