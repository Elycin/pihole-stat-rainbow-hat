#!/bin/bash

SERVICE="pihole-stat-rainbow-hat"

echo "Editing service file to contain current working directory: $PWD"
sed -i 's/{directory}/"$PWD"/g' $PWD/$SERVICE.service

echo "Copying service file into /etc/systemd/system/..."
sudo cp $PWD/$SERVICE.service  /etc/systemd/system/$SERVICE.service

echo "Restarting Systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling run-at-boot for $SERVICE..."
sudo systemctl enable $SERVICE

echo "Starting service..."
sudo systemctl start $SERVICE