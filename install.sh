#!/bin/bash
HERE=$(dirname $0)
cd "$HERE"
set -eo pipefail

echo "Install required packages"
apt-get install -y fluidsynth fluid-soundfont-gm curl

echo "Install service file"
cp -f pipiano.service /etc/systemd/system
systemctl daemon-reload
systemctl enable pipiano
