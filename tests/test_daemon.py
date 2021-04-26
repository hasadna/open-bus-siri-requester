import os
import json
import shutil
import datetime

import pytz

from open_bus_siri_requester import daemon


def test():
    shutil.rmtree('.data', ignore_errors=True)
    mock_calls = []

    def mock_store(siri_snapshot, store_datetime, upload=False):
        mock_calls.append(('store', [siri_snapshot, store_datetime, upload]))
        return 'mock-snapshot-id'

    def mock_request():
        mock_calls.append(('request', []))
        return {'foo': 'bar'}

    now = datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=pytz.UTC)
    last_cleanup_datetime = datetime.datetime(2020, 5, 4, 3, 2, 1, tzinfo=pytz.UTC)
    daemon.run_single_iteration(now, last_cleanup_datetime, mock_store, mock_request)
    assert mock_calls == [
        ('request', []),
        ('store', [{'foo': 'bar'}, datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), True])
    ]
    with open(os.path.join('.data/siri/daemon_status.json')) as f:
        assert json.load(f) == {
            'last_cleanup_datetime_utc': '2020-05-04 03:02:01',
            'last_datetime_utc': '2020-01-02 03:04:05',
            'last_snapshot_id': 'mock-snapshot-id'
        }

