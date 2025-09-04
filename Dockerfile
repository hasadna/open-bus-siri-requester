# Pulled Sep 4, 2025
FROM --platform=linux/amd64 python:3.8@sha256:d411270700143fa2683cc8264d9fa5d3279fd3b6afff62ae81ea2f9d070e390c
RUN apt-get update && apt-get install -y brotli
RUN pip install --upgrade pip
WORKDIR /srv
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY setup.py ./
COPY open_bus_siri_requester ./open_bus_siri_requester
RUN pip install -e .
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["open-bus-siri-requester", "daemon-start"]