# Open Bus SIRI Requester

Request and store SIRI real-time snapshots

## Required environment variables

* `OPEN_BUS_MOT_KEY`: a key used to authenticate with MOT (Ministry of Transportation) servers
* `OPEN_BUS_SSH_TUNNEL_PRIVATE_KEY_FILE`: Private SSH key file used to open a tunnel to proxy server which is authorized to access MOT servers
* `OPEN_BUS_SSH_TUNNEL_SERVER_IP`: IP of the proxy server which is authorized to access MOT servers
* `OPEN_BUS_S3_ENDPOINT`: S3 endpoint used to store all snapshots to
* `OPEN_BUS_S3_ACCESS_KEY_ID`: S3 access key used to store all snapshots to
* `OPEN_BUS_S3_SECRET_ACCESS_KEY`: S3 secret access key used to store all snapshots to
* `OPEN_BUS_S3_BUCKET`: S3 bucket used to store all snapshots to

## Development using the Docker Compose environment

This is the easiest option to start development, follow these instructions: https://github.com/hasadna/open-bus-pipelines/blob/main/README.md#siri-requester

For local development, see the additional functionality section: `Develop siri-requester from a local clone`

## Development using local Python interpreter

It's much easier to use the Docker Compose environment, but the following can be
refferd to for more details regarding the internal processes and for development
using your local Python interpreter. 

### Install

Install Brotli for compression

```
sudo apt-get install brotli
```

Create virtualenv (Python 3.8)

```
python3.8 -m venv venv
```

Install dependencies

```
venv/bin/python -m pip install -r requirements.txt
```

Install the Python module

```
venv/bin/python -m pip install -e .
```


### Configure

Create the following `.env` file or get it from a friend:

```
export OPEN_BUS_MOT_KEY=
export OPEN_BUS_SSH_TUNNEL_PRIVATE_KEY_FILE=
export OPEN_BUS_SSH_TUNNEL_SERVER_IP=
export OPEN_BUS_S3_ENDPOINT=
export OPEN_BUS_S3_ACCESS_KEY_ID=
export OPEN_BUS_S3_SECRET_ACCESS_KEY=
export OPEN_BUS_S3_BUCKET=
```

* `OPEN_BUS_SSH_TUNNEL_PRIVATE_KEY_FILE` should point to the local path to the private key file for ssh tunnelling
  * Make sure it has the correct permissions: `chmod 400 $OPEN_BUS_SSH_TUNNEL_PRIVATE_KEY_FILE`


### Use

Activate the virtualenv and source the .env file

```
. venv/bin/activate
source .env
```

Check the CLI help message

```
open-bus-siri-requester
```


### Running Unit Tests

Install test requirements

```
pip install -r tests/requirements.txt
```

Run tests

```
pytest
```


### Using Docker

Source the env vars created for local development

```
source .env
```

Build and run requester daemon

```
docker build -t open-bus-siri-requester . &&\
docker run --rm -it \
    -e OPEN_BUS_MOT_KEY -e OPEN_BUS_SSH_TUNNEL_SERVER_IP -e OPEN_BUS_SSH_TUNNEL_PRIVATE_KEY_FILE=/tmp/ssh_tunnel.key \
    -e OPEN_BUS_S3_ENDPOINT_URL -e OPEN_BUS_S3_ACCESS_KEY_ID -e OPEN_BUS_S3_SECRET_ACCESS_KEY -e OPEN_BUS_S3_BUCKET \
    -v $OPEN_BUS_SSH_TUNNEL_PRIVATE_KEY_FILE:/tmp/ssh_tunnel.key -v `pwd`/.data:/srv/.data \
    open-bus-siri-requester
```

Build and run nginx server for serving the requested files + status

```
docker build -t open-bus-siri-requester-nginx nginx &&\
docker run --rm -it -p 8080:80 -v `pwd`/.data:/srv open-bus-siri-requester-nginx
```

Browse the files at http://localhost:8080
s