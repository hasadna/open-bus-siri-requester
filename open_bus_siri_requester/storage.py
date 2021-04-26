import os
import json
import glob
import shutil
import datetime
import tempfile
import subprocess

import pytz
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from . import config


def get_s3_resource(retry_max_attempts=10, connect_timeout=15, read_timeout=60):
    return boto3.resource(
        's3', endpoint_url=config.OPEN_BUS_S3_ENDPOINT_URL,
        aws_access_key_id=config.OPEN_BUS_S3_ACCESS_KEY_ID,
        aws_secret_access_key=config.OPEN_BUS_S3_SECRET_ACCESS_KEY,
        # region_name='us-east-1',
        config=Config(
            signature_version='s3v4',
            retries={'max_attempts': retry_max_attempts, 'mode': 'standard'},
            connect_timeout=connect_timeout, read_timeout=read_timeout
        )
    )


def upload_snapshot(snapshot_id):
    filename = os.path.join(config.OPEN_BUS_SIRI_STORAGE_ROOTPATH, snapshot_id + '.br')
    target_key = os.path.join(config.OPEN_BUS_S3_PATH_PREFIX, snapshot_id + '.br')
    print("Uploading {} -> {}".format(filename, target_key))
    s3 = get_s3_resource()
    bucket = s3.Bucket(config.OPEN_BUS_S3_BUCKET)
    bucket.upload_file(filename, target_key)


def store(siri_snapshot, store_datetime, upload=False):
    snapshot_id = store_datetime.strftime('%Y/%m/%d/%H/%M')
    filename = os.path.join(config.OPEN_BUS_SIRI_STORAGE_ROOTPATH, snapshot_id + '.br')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, 'temp.json'), 'w') as f:
            json.dump(siri_snapshot, f)
        ret, out = subprocess.getstatusoutput('cat {} | brotli -c > {}'.format(os.path.join(tmpdir, 'temp.json'), os.path.join(tmpdir, 'temp.br')))
        assert ret == 0, out
        shutil.move(os.path.join(tmpdir, 'temp.br'), filename)
    if upload:
        upload_snapshot(snapshot_id)
    return snapshot_id


def list(snapshot_id_prefix=None, limit=200):
    i = 0
    path_param = [config.OPEN_BUS_SIRI_STORAGE_ROOTPATH]
    if snapshot_id_prefix:
        path_param.append(snapshot_id_prefix)
    path_param.append('**/*.br')
    for filename in glob.iglob(os.path.join(*path_param), recursive=True):
        snapshot_id = filename.replace(os.path.join(config.OPEN_BUS_SIRI_STORAGE_ROOTPATH, ''), '').replace('.br', '')
        yield snapshot_id
        i += 1
        if i == limit:
            break


def read(snapshot_id):
    filename = os.path.join(config.OPEN_BUS_SIRI_STORAGE_ROOTPATH, snapshot_id + '.br')
    ret, out = subprocess.getstatusoutput('cat {} | brotli -d'.format(filename))
    assert ret == 0, out
    return json.loads(out)


def cleanup():
    now = datetime.datetime.now(pytz.UTC)
    last_week = now - datetime.timedelta(days=7)
    for d in range(30):
        path_prefix = (last_week - datetime.timedelta(days=d)).strftime('%Y/%m/%d')
        path = os.path.join(config.OPEN_BUS_SIRI_STORAGE_ROOTPATH, path_prefix)
        if os.path.exists(path):
            print("Removing path: {}".format(path))
            shutil.rmtree(path)
            path_prefix = (last_week - datetime.timedelta(days=d)).strftime('%Y/%m')
            path = os.path.join(config.OPEN_BUS_SIRI_STORAGE_ROOTPATH, path_prefix)
            if len(glob.glob(path + '/*')) == 0:
                os.rmdir(path)
            path_prefix = (last_week - datetime.timedelta(days=d)).strftime('%Y')
            path = os.path.join(config.OPEN_BUS_SIRI_STORAGE_ROOTPATH, path_prefix)
            if len(glob.glob(path + '/*')) == 0:
                os.rmdir(path)
