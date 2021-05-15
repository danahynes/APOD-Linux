#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: uninstall.sh                                         /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# show some progress
# NB: first call with sudo to ask for password on its own line (aesthetics)
sudo echo "Uninstalling APOD_Linux..."

# stop the unlock listener
echo -n "Stopping unlock listener... "
sudo pkill -f "/usr/bin/apod_linux_unlock.sh"
echo "Done"

# delete dirs/files from locations
echo -n "Deleting all data and scripts... "
sudo rm -rf "${HOME}/.apod_linux"
sudo rm -f "/etc/profile.d/apod_linux_login.sh"
sudo rm -f "/usr/bin/apod_linux_unlock.sh"
sudo rm -f "/usr/bin/apod_linux.py"
sudo rm -f "/usr/bin/apod_linux_caption.sh"
echo "Done"

# show that we are done
echo "APOD_Linux uninstalled"

# -)
