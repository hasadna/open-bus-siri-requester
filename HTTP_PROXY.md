# HTTP Proxy

We use an HTTP Proxy to access the SIRI data from MOT allowed IP

The proxy is running on server hasadna-proxy1 (see hasadna-iac for terraform configuration setting it up and to get access)

To access from local PC you need to create an SSH tunnel to this server:

```
ssh hasadna-proxy1 -L 9999:172.16.0.5:9999 -N
```

Then set the HTTP_PROXY and HTTPS_PROXY environment variables to point to the local end of the tunnel:

```
export HTTP_PROXY=http://localhost:9999
export HTTPS_PROXY=http://localhost:9999
```
