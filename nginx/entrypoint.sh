#!/usr/bin/env bash

if [ "${SIRI_REQUESTER_HEALTH_URL}" == "" ]; then
  echo missing SIRI_REQUESTER_HEALTH_URL
  exit 1
fi

echo "SIRI_REQUESTER_HEALTH_URL=${SIRI_REQUESTER_HEALTH_URL}" &&\
sed -i "s;SIRI_REQUESTER_HEALTH_URL;${SIRI_REQUESTER_HEALTH_URL};g" "/etc/nginx/conf.d/default.conf" &&\
exec nginx -g "daemon off;"
