#!/usr/bin/env bash
source ~/oprint/bin/activate
cd ~/OctoRelay
python setup.py develop
sudo service octoprint restart
tail -f ~/.octoprint/logs/octoprint.log | sed '/OctoRelay plugin started$/ q'
