import json
import datetime

import pytz
import click

from . import requester
from . import storage
from . import daemon
from . import health_daemon


@click.group(context_settings={'max_content_width': 200})
def main():
    """Open Bus SIRI"""
    pass


@main.command()
def requester_request():
    """Make a single request to get the SIRI Snapshot data via ssh tunnel, prints the response json"""
    print(json.dumps(requester.request(), indent=2))


@main.command()
@click.option('--upload', is_flag=True)
def storage_store(upload):
    """Requests and stores a single SIRI Snapshot for current timestamp"""
    print(storage.store(requester.request(), datetime.datetime.now(pytz.UTC), upload=upload))


@main.command()
@click.argument('SNAPSHOT_ID_PREFIX', required=False)
@click.option('--limit', default=200)
def storage_list(snapshot_id_prefix, limit):
    """List up to 200 SIRI Snapshots from storage"""
    for snapshot_id in storage.list(snapshot_id_prefix, limit=limit):
        print(snapshot_id)


@main.command()
@click.argument('SNAPSHOT_ID')
def storage_read(snapshot_id):
    """reads and outputs the json of a single snapshot"""
    print(json.dumps(storage.read(snapshot_id)))


@main.command()
def storage_cleanup():
    storage.cleanup()


@main.command()
def daemon_start():
    """Starts the daemon which periodically requests and stores snapshots"""
    daemon.start()


@main.command()
def health_daemon_start():
    """Starts the health daemon which exposes an HTTP page that returns health status"""
    health_daemon.start()


@main.command()
def seconds_since_last_snapshot():
    print(storage.get_seconds_since_last_snapshot())
