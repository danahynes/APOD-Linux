#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: uninstall.sh                                         /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# remove the cron job
croncmd="python3 /usr/bin/apod_linux.py"
( crontab -l | grep -v -F "$croncmd" ) | crontab -

# delete the script
sudo rm -rf /usr/bin/apod_linux.py

# N.B. we leave the hidden directory with the current wallpaper in it so the
# desktop doesn't go black

# -)
