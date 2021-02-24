#! /bin/sh
#------------------------------------------------------------------------------#
# Filename: apod_linux.sh                                        /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# this file goes in /etc/cron.daily to run once a day or on boot
# it is also important that the shebang uses sh and not bash!

# run the script
python3 /usr/bin/apod_linux.py

# -)
