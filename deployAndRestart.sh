#!/usr/bin/env bash
rsync -avzh . pi@octopi.local:~/OctoRelay
ssh pi@octopi.local "~/OctoRelay/installOnPiAndRestart.sh"
