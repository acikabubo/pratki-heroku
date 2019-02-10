#!/bin/bash

# Make logs directories
mkdir -p -v logs/beat
mkdir -p -v logs/celery
mkdir -p -v logs/flower
mkdir -p -v logs/server
mkdir -p -v logs/supervisor

# Starting supervisor service
sudo service supervisor start

# Get and update supervisorctl configurations
supervisorctl reread
echo
supervisorctl update
sleep 5  # wait for 5 seconds

# Check status and check if everything is started
supervisorctl status
echo
