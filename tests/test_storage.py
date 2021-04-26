import os
import json
import shutil
import datetime
import subprocess

import pytz

from open_bus_siri_requester import storage


def test_store():
    shutil.rmtree('.data')
    siri_snapshot = {'foo': 'bar'}
    store_datetime = datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=pytz.UTC)
    mock_calls = []

    def mock_upload_snapshot(snapshot_id):
        mock_calls.append(('upload_snapshot', [snapshot_id]))

    snapshot_id = storage.store(siri_snapshot, store_datetime, upload=True, upload_snapshot_callback=mock_upload_snapshot)
    assert snapshot_id == '2020/01/02/03/04'
    filename = '.data/siri/2020/01/02/03/04.br'
    assert os.path.exists(filename)
    ret, out = subprocess.getstatusoutput('cat .data/siri/2020/01/02/03/04.br | brotli -d')
    assert ret == 0
    assert json.loads(out) == siri_snapshot
    assert mock_calls == [('upload_snapshot', ['2020/01/02/03/04'])]
    del mock_calls[0]
    storage.store(siri_snapshot, store_datetime, upload=False, upload_snapshot_callback=mock_upload_snapshot)
    assert mock_calls == []


def test_list():
    shutil.rmtree('.data')
    siri_snapshot = {'foo': 'bar'}
    store_datetime = datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=pytz.UTC)
    expected_snapshot_ids = set()
    expected_snapshot_ids.add(storage.store(siri_snapshot, store_datetime, upload=False))
    expected_snapshot_ids.add(storage.store(siri_snapshot, store_datetime + datetime.timedelta(days=60), upload=False))
    expected_snapshot_ids.add(storage.store(siri_snapshot, store_datetime + datetime.timedelta(days=30), upload=False))
    expected_snapshot_ids.add(storage.store(siri_snapshot, store_datetime + datetime.timedelta(days=10), upload=False))
    expected_snapshot_ids.add(storage.store(siri_snapshot, store_datetime + datetime.timedelta(days=1), upload=False))
    expected_snapshot_ids.add(storage.store(siri_snapshot, store_datetime + datetime.timedelta(hours=10), upload=False))
    expected_snapshot_ids.add(storage.store(siri_snapshot, store_datetime + datetime.timedelta(hours=5), upload=False))
    expected_snapshot_ids.add(storage.store(siri_snapshot, store_datetime + datetime.timedelta(hours=1), upload=False))
    expected_snapshot_ids.add(storage.store(siri_snapshot, store_datetime + datetime.timedelta(minutes=1), upload=False))
    expected_snapshot_ids.add(storage.store(siri_snapshot, store_datetime + datetime.timedelta(minutes=30), upload=False))
    expected_snapshot_ids.add(storage.store(siri_snapshot, store_datetime + datetime.timedelta(minutes=40), upload=False))
    assert set(storage.list()) == expected_snapshot_ids
    assert len(set(storage.list(limit=5))) == 5
    assert list(storage.list(limit=1))[0] in expected_snapshot_ids
    assert set(storage.list(snapshot_id_prefix='2020/01/02/04')) == {'2020/01/02/04/04'}


def test_read():
    shutil.rmtree('.data')
    siri_snapshot = {'foo': 'bar'}
    store_datetime = datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=pytz.UTC)
    snapshot_id = storage.store(siri_snapshot, store_datetime, upload=False)
    assert storage.read(snapshot_id) == siri_snapshot


def test_cleanup():
    shutil.rmtree('.data')
    siri_snapshot = {'foo': 'bar'}
    now = datetime.datetime.now(pytz.UTC)
    expected_after_delete = set()
    expected_after_delete.add(storage.store(siri_snapshot, now, upload=False))
    expected_after_delete.add(storage.store(siri_snapshot, now - datetime.timedelta(days=6), upload=False))
    storage.store(siri_snapshot, now - datetime.timedelta(days=7), upload=False)
    storage.store(siri_snapshot, now - datetime.timedelta(days=8), upload=False)
    storage.store(siri_snapshot, now - datetime.timedelta(days=29), upload=False)
    storage.store(siri_snapshot, now - datetime.timedelta(days=30), upload=False)
    assert len(set(storage.list())) == 6
    storage.cleanup()
    assert set(set(storage.list())) == expected_after_delete

