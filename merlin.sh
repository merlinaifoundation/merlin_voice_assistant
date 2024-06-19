#!/bin/bash
pulseaudio --start
sleep 0.1
cd /home/merlin/Documents/Merlin/merlin_voice_assistant
git stash
git pull
python3 -m venv myenv
source /home/merlin/Documents/Merlin/merlin_voice_assistant/myenv/bin/activate
pip install -r requirements.txt
python3 /home/merlin/Documents/Merlin/merlin_voice_assistant/main.py
