#!/bin/bash

$SYSTEMDPATH="/etc/systemd/system"
SERVICE="pihole-stat-rainbow-hat"
PYTHONPATH=$(which python3)

echo "Installation directory will be $PWD"

echo "Copying service file into $SYSTEMDPATH ..."
sudo cp $PWD/$SERVICE.service  $SYSTEMDPATH/$SERVICE.service

echo "Editing service file ..."
sed -i "s|{directory}|$PWD|g" $SYSTEMDPATH/$SERVICE.service
sed -i "s|{python3}|$PYTHONPATH|g" $SYSTEMDPATH/$SERVICE.service

echo "Restarting Systemd daemon..."
sudo systemctl daemon-reload

echo "Script has successfully created a systemd service."