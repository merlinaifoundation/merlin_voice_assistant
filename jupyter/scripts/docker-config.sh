# Check service is running ...
#!/bin/bash


{ echo "[Service]";
  echo "ExecStart=";
  echo "ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2376";
} > $HOME/docker-override.conf

env SYSTEMD_EDITOR="cp $HOME/docker-override.conf" systemctl edit docker.service

cat > /etc/docker/daemon.json <<EOF
{
    "tls": true,
    "tlscacert": "/etc/docker/ca.pem",
    "tlscert": "/etc/docker/server-cert.pem",
    "tlskey": "/etc/docker/server-key.pem",
    "tlsverify": true
}
EOF
