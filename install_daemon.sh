#!/bin/bash
su
cat daemon > /etc/systemd/system/test.service
#chmod +x merlin.sh
systemctl daemon-reload
systemctl enable test.service
systemctl status test.service