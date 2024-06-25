#!/bin/bash
#INTERFACE="wlp0s20f3u1"
IP="auto"
INTERFACE="wlan0"  # Replace with your wireless interface name

# Bring up the interface
ifconfig $INTERFACE down

# Set the ESSID and WEP key
iwconfig $INTERFACE power off
iwconfig $INTERFACE txpower auto
iwconfig $INTERFACE retry 30
#iwconfig $INTERFACE ap auto
#iwconfig $INTERFACE modulation 11g
iwconfig $INTERFACE power on

iwconfig

ifconfig $INTERFACE $IP
ifconfig $INTERFACE up

ip link set $INTERFACE down
ip link set $INTERFACE up
ip addr show

rm -rf "/var/run/wpa_supplicant/$INTERACE"
wpa_supplicant -B -Dwext,nl80211 -i$INTERFACE -cwpa_supplicant.conf

# Optional: Restart network services
#systemctl stop networking
#systemctl start networking
#systemctl status networking



