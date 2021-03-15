#!/usr/bin/env bash
rsync -avzh --exclude='.git/' --exclude='.DS_Store' --exclude='deployAndRestart.sh' --delete . pi@octopi.local:~/OctoRelay
ssh pi@octopi.local "~/OctoRelay/installOnPiAndRestart.sh"
