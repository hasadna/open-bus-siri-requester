import os
import json
import time
import datetime

import pytz

from . import config
from . import storage
from . import requester
from .graceful_killer import GracefulKiller


def run_single_iteration(now, last_cleanup_datetime, store_callback=None, requester_callback=None):
    if not store_callback:
        store_callback = storage.store
    if not requester_callback:
        requester_callback = requester.request
    snapshot_id = store_callback(requester_callback(), now, upload=True)
    print("Stored snapshot: {}".format(snapshot_id))
    os.makedirs(config.OPEN_BUS_SIRI_STORAGE_ROOTPATH, exist_ok=True)
    with open(os.path.join(config.OPEN_BUS_SIRI_STORAGE_ROOTPATH, 'daemon_status.json'), 'w') as f:
        json.dump({
            'last_snapshot_id': snapshot_id,
            'last_datetime_utc': now.strftime('%Y-%m-%d %H:%M:%S'),
            'last_cleanup_datetime_utc': last_cleanup_datetime.strftime('%Y-%m-%d %H:%M:%S'),
        }, f)
    return now


def start():
    graceful_killer = GracefulKiller()
    last_datetime = None
    last_cleanup_datetime = None
    if os.path.exists(os.path.join(config.OPEN_BUS_SIRI_STORAGE_ROOTPATH, 'daemon_status.json')):
        with open(os.path.join(config.OPEN_BUS_SIRI_STORAGE_ROOTPATH, 'daemon_status.json')) as f:
            last_daemon_status = json.load(f)
        if last_daemon_status.get('last_cleanup_datetime_utc'):
            last_cleanup_datetime = datetime.datetime.strptime(last_daemon_status['last_cleanup_datetime_utc'] + 'z+0000', '%Y-%m-%d %H:%M:%Sz%z')
    while not graceful_killer.kill_now:
        now = datetime.datetime.now(pytz.UTC)
        if last_cleanup_datetime is None or (now - last_cleanup_datetime).total_seconds() >= 60*60*24:
            storage.cleanup()
            last_cleanup_datetime = now
        if last_datetime is None or (now - last_datetime).total_seconds() >= 60:
            run_single_iteration(now, last_cleanup_datetime)
            last_datetime = now
        time.sleep(1)
