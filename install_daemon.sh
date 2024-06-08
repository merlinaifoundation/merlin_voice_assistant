sudo cp daemon /etc/systemd/system/test.service
sudo systemctl daemon-reload
sudo systemctl enable test.service