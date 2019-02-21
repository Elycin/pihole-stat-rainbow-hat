#!/bin/bash

SERVICE="pihole-stat-rainbow-hat"
PYTHONPATH=$(which python3)

echo "Installation directory will be $PWD"

echo "Editing service file ..."
sed -i "s|{directory}|$PWD|g" $PWD/$SERVICE.service
sed -i "s|{python3}|$PYTHONPATH|g" $PWD/$SERVICE.service

echo "Copying service file into /etc/systemd/system/ ..."
sudo cp $PWD/$SERVICE.service  /etc/systemd/system/$SERVICE.service

echo "Restarting Systemd daemon..."
sudo systemctl daemon-reload

echo "Script has successfully created a systemd service."