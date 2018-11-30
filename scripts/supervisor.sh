#!/bin/bash

# Starting supervisor service
sudo service supervisor start  # starting supervisor service

# Get and update supervisorctl configurations
supervisorctl reread
echo
supervisorctl update
sleep 5  # wait for 5 seconds

# Check status and check if everything is started
supervisorctl status
echo
