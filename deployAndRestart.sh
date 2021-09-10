#!/usr/bin/env bash
target="pi@octopi-dev.local";
echo "deploy to octopi: ${target}"
rsync -avzh --exclude='.git/' --exclude='.DS_Store' --exclude='deployAndRestart.sh' --delete . ${target}:~/OctoRelay
ssh ${target} "~/OctoRelay/installOnPiAndRestart.sh"
