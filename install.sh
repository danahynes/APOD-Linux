#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: install.sh                                           /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# copy the script to the location
sudo cp ./apod_linux.py /usr/bin

# add the cron job to run every day at midnight
croncmd="python3 /usr/bin/apod_linux.py"
cronjob="0 0 * * * $croncmd"
(crontab -l ; echo "$cronjob") | sort - | uniq - | crontab -

# start now
python3 /usr/bin/apod_linux.py

# -)
