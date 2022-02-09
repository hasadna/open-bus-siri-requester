import os

# a key used to authenticate with MOT (Ministry of Transportation) servers
OPEN_BUS_MOT_KEY = os.environ.get('OPEN_BUS_MOT_KEY')
# Private SSH key file used to open a tunnel to proxy server which is authorized to access MOT servers
OPEN_BUS_SSH_TUNNEL_PRIVATE_KEY_FILE = os.environ.get('OPEN_BUS_SSH_TUNNEL_PRIVATE_KEY_FILE')
# IP of the proxy server which is authorized to access MOT servers
OPEN_BUS_SSH_TUNNEL_SERVER_IP = os.environ.get('OPEN_BUS_SSH_TUNNEL_SERVER_IP')

OPEN_BUS_SIRI_STORAGE_ROOTPATH = os.environ.get('OPEN_BUS_SIRI_STORAGE_ROOTPATH') or '.data/siri'

# S3 credentials and connection details used to store snapshots
OPEN_BUS_S3_ENDPOINT_URL = os.environ.get('OPEN_BUS_S3_ENDPOINT_URL')
OPEN_BUS_S3_ACCESS_KEY_ID = os.environ.get('OPEN_BUS_S3_ACCESS_KEY_ID')
OPEN_BUS_S3_SECRET_ACCESS_KEY = os.environ.get('OPEN_BUS_S3_SECRET_ACCESS_KEY')
OPEN_BUS_S3_BUCKET = os.environ.get('OPEN_BUS_S3_BUCKET')
OPEN_BUS_S3_PATH_PREFIX = os.environ.get('OPEN_BUS_S3_PATH_PREFIX', 'stride-siri-requester')

# timeout of the request call to the MOT server
OPEN_BUS_REQUESTER_TIMEOUT_SECONDS = int(os.environ.get('OPEN_BUS_REQUESTER_TIMEOUT_SECONDS') or '120')

HEALTH_DAEMON_PORT = int(os.environ.get('HEALTH_DAEMON_PORT') or '8081')
HEALTH_DAEMON_MAX_SECONDS_SINCE_LAST_SNAPSHOT = int(os.environ.get('HEALTH_DAEMON_MAX_SECONDS_SINCE_LAST_SNAPSHOT') or '240')
