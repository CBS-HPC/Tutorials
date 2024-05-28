#!/bin/bash

# Installing dependencies
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install libncurses5 libncurses5:i386 -y

# Set stata17 on UNIX path
export PATH="/work/stata17:$PATH"