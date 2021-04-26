# SSH Tunnel

We use an SSH tunnel to access the SIRI data from MOT allowed IP

## Creating an SSH User for tunnelling

Generate an SSH key and store somewhere safe

```
ssh-keygen -t ed25519 -C "obus-ssh-tunnel"
```

SSH to the allowed server (obus-dev-4) and run the following commands:

Set the following in `/etc/ssh/sshd_config` and reload the ssh server

```
AllowTcpForwarding yes
PermitOpen any
```

Create sshtunnel user

```
sudo useradd sshtunnel -m -d /home/sshtunnel -s /bin/true
```

Set authrized keys (replace PUBLIC_KEY with the public key you generated)

```
sudo mkdir /home/sshtunnel/.ssh
sudo chown sshtunnel /home/sshtunnel/.ssh
echo PUBLIC_KEY | sudo tee -a /home/sshtunnel/.ssh/authorized_keys
sudo chown sshtunnel /home/sshtunnel/.ssh/authorized_keys
```

From your local PC, start the tunnel (replace SECRET_KEY with the secret key file and SERVER_IP with the tunnelling server ip)

```
ssh -D 8123 -C -N -i SECRET_KEY sshtunnel@SERVER_IP
```

Keep it open and in a new terminal run:

```
curl --socks5-hostname "127.0.0.1:8123" ifconfig.me
```

You should get the server IP in response
