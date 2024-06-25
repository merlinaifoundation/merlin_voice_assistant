#!/bin/bash
cat daemon_wifi_merlin > /etc/systemd/system/wifi_merlin.service

systemctl daemon-reload
systemctl enable wifi_merlin.service
systemctl status wifi_merlin.service
