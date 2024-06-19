#!/bin/bash
sudo systemctl disable test.service
sudo cat daemon > /etc/systemd/system/test.service
sudo chmod +x merlin.sh
sudo systemctl daemon-reload
sudo systemctl enable test.service
sudo systemctl status test.service