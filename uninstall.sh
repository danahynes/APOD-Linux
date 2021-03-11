#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: uninstall.sh                                         /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# get name of current user for hidden dir
user=$(whoami)
if [ "${user}" == "root" ]
then
  echo "Can't uninstall as root, don't run with sudo..."
  exit 1
fi

# delete files from locations
sudo rm -rf /etc/profile.d/apod_linux_login.sh
sudo rm -rf /lib/systemd/system-sleep/apod_linux_wake.sh
sudo rm -rf /usr/bin/apod_linux.py
sudo rm -rf "/home/${user}/.apod_linux"

# -)
