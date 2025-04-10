#!/bin/bash

# Activate conda environment
source /root/anaconda3/bin/activate occenv

# Navigate to project directory
cd /www/wwwroot/occ.momaking.com

# Kill old Python processes
pkill -f "python main.py"

# Start new Flask application in background
# python main.py
nohup python main.py > /dev/null 2>&1 &