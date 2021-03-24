#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: uninstall.sh                                         /          \  #
# Project : APOD_Linux                                          |     ()     | #
# Date    : 02/21/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# get name of current user for hidden dir
user=''
user_test=$(whoami)
if [ "${user_test}" == "root" ]
then
  user=${SUDO_USER}
else
  user=${user_test}
fi

# delete files from locations
sudo rm -rf "/home/${user}/.apod_linux"
sudo rm -rf /etc/profile.d/apod_linux_login.sh
sudo rm -rf /lib/systemd/system-sleep/apod_linux_wake.sh
sudo rm -rf /usr/bin/apod_linux.py

# -)
